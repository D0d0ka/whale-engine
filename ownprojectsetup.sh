#!/bin/bash

set -e

REPO="https://github.com/D0d0ka/whale-engine.git"
TEMP_DIR="whale-engine-temp"

echo "Cloning whale-engine..."
git clone "$REPO" "$TEMP_DIR"

echo "Copying WhaleEngine..."
cp -r "$TEMP_DIR/WhaleEngine" .

echo "Copying requirements..."
cp -r "$TEMP_DIR/requirements" .

echo "Deleting clone..."
rm -rf "$TEMP_DIR"

echo "Done!"