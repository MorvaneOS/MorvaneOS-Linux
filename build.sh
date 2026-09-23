#!/usr/bin/env bash
# Builds the MorvaneOS ISO. Run inside WSL: bash build.sh
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
WS="$HOME/artools-workspace"

# Sync profiles from the repo into the artools workspace (Linux filesystem)
rm -rf "$WS/iso-profiles"
cp -r "$REPO/iso-profiles" "$WS/iso-profiles"

buildiso -p morvane -i runit

mkdir -p "$REPO/out"
cp "$WS"/iso/morvane/*.iso "$REPO/out/"
echo "Done: ISO copied to out/"
