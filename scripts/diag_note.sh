#!/usr/bin/env bash
set -euo pipefail

OUTDIR="/home/pizero2w/tundra-alarm-ecu/notes"
mkdir -p "$OUTDIR"
STAMP="$(date +%F_%H%M%S)"
OUTFILE="$OUTDIR/stack_health_${STAMP}.txt"

CONFIG_FILE="/boot/firmware/config.txt"
REPO_DIR="/home/pizero2w/tundra-alarm-ecu"

svc_state() {
  local svc="$1"
  if systemctl cat "$svc" >/dev/null 2>&1; then
    systemctl is-active "$svc" 2>/dev/null || true
  else
    echo "not installed"
  fi
}

mpu_check() {
  if ! command -v i2cdetect >/dev/null 2>&1; then
    echo "i2c-tools not installed"
    return
  fi

  local scan
  scan="$(i2cdetect -y 1 2>/dev/null || true)"
  echo "$scan" | awk '
    NR > 1 {
      for (i = 2; i <= NF; i++) {
        if ($i == "68" || $i == "UU") found=1
      }
    }
    END {
      if (found) print "MPU-6050 present on bus (0x68 or claimed as UU)"
      else print "MPU-6050 not seen at 0x68"
    }
  '
}

{
  echo "TUNDRA STACK HEALTH NOTE"
  echo "Generated: $(date)"
  echo

  echo "=== HOST ==="
  echo "Hostname: $(hostname)"
  echo "Uptime: $(uptime -p)"
  echo

  echo "=== SERVICES ==="
  echo "gps2mqtt.service: $(svc_state gps2mqtt.service)"
  echo "alarm_core.service: $(svc_state alarm_core.service)"
  echo

  echo "=== UART / GPS ==="
  echo -n "/dev/serial0 -> "
  readlink -f /dev/serial0 || echo "missing"
  echo "gps2mqtt status: $(systemctl is-active gps2mqtt.service 2>/dev/null || echo unknown)"
  echo

  echo "=== I2C / MPU ==="
  mpu_check
  echo

  echo "=== CAN ==="
  ip -br link show type can || echo "No CAN interfaces found"
  echo
  for iface in can0 can1; do
    if ip link show "$iface" >/dev/null 2>&1; then
      echo "--- $iface details ---"
      ip -details link show "$iface" || true
      echo
    fi
  done

  echo "=== MCP2515 INIT LOG ==="
  dmesg | grep -iE 'mcp2515|mcp251x|CAN device driver interface|spi0\.[01].*can[01]' || true
  echo

  echo "=== CONFIG SNIPPET ==="
  grep -nE 'mcp2515|spi=' "$CONFIG_FILE" || true
  echo

  echo "=== REPO STATUS ==="
  cd "$REPO_DIR"
  git status --short || true
  echo

} | tee "$OUTFILE"

echo
echo "Saved note to: $OUTFILE"
