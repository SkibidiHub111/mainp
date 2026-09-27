#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

cd "$(dirname "$0")"
url="https://banana-hub.xyz/scripts/kaitun_levi.lua"
input="kaitun_levi.lua"
output="output/kaitun_levi.deob.lua"

command -v curl >/dev/null || pkg install -y curl
curl -fL "$url" -o "$input"
mkdir -p output
deob-luraph "$input" --deep -o "$output"

echo
echo "Output: $output"
if [ -f "$output.report.txt" ]; then
  echo "Quality report: $output.report.txt"
  cat "$output.report.txt"
fi
