#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

echo "[1/4] Installing Termux build dependencies..."
pkg update -y
pkg install -y nodejs python git cmake ninja clang make

echo "[2/4] Building patched Luau + luau-ast for this phone..."
python3 build_luau.py

echo "[3/4] Checking runtime..."
./bin/luau --help >/dev/null
./bin/luau-ast --help >/dev/null
node --check deob.js

echo "[4/4] Installing the deob-luraph command..."
mkdir -p "$PREFIX/bin"
chmod +x deob-luraph
ln -sfn "$(pwd)/deob-luraph" "$PREFIX/bin/deob-luraph"

echo
echo "Installed. Example:"
echo "  deob-luraph input.lua --deep -o output.lua"
