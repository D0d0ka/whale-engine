#!/bin/bash

set -e

REPO="https://github.com/D0d0ka/whale-engine.git"
TEMP_DIR="whale-engine-temp"

rm -rf "WhaleEngine"

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed!"
    echo "Please install Git before running this script."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python is not installed!"
    echo "Please install Python before running this script."
    exit 1
fi

echo "Cloning whale-engine..."

git clone "$REPO" "$TEMP_DIR"

echo "Copying WhaleEngine..."

cp -r "$TEMP_DIR/WhaleEngine" .

# Create main.py if it does not exist
if [ ! -f "main.py" ]; then
    echo "main.py not found. Creating it from WhaleEngine/AppBase.py..."
    cp "$TEMP_DIR/AppBase.py" "main.py"
fi

if [ ! -f "NOTICE" ]; then
    echo "NOTICE not found. Creating it from WhaleEngine/NOTICE..."
    cp "$TEMP_DIR/NOTICE" "NOTICE"
fi

if [ ! -f ".gitignore" ]; then
    echo ".gitignore not found. Creating it from WhaleEngine/.gitignore..."
    cp "$TEMP_DIR/setup/.gitignoretemplate" ".gitignore"
fi

echo "Deleting clone..."

rm -rf "$TEMP_DIR"

echo "Done!"