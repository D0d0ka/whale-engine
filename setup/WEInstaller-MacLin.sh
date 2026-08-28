#!/bin/bash

set -e

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed!"
    echo "Please install Git before running this script."
    echo "You can download it from https://git-scm.com/downloads"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python is not installed!"
    echo "Please install Python before running this script."
    echo "You can download it from https://www.python.org/downloads/"
    exit 1
fi

REPO="https://github.com/D0d0ka/whale-engine.git"
TEMP_DIR="whale-engine-temp"

function install_other_dependencies() {
    read -p "Do you wan't to install OpenGL dependencies now? (y/n): " install_opengl
    if [ "$install_opengl" = "y" ]; then
        echo "Installing OpenGL dependencies..."
        pip install -r WhaleEngine/requirements/openGLrequirements.txt
        echo "OpenGL dependencies installed."
    fi

    read -p "Do you wan't to install Vulkan dependencies now? (y/n): " install_vulkan
    if [ "$install_vulkan" = "y" ]; then
        echo "Installing Vulkan dependencies..."
        pip install -r WhaleEngine/requirements/vulcanrequirements.txt
        echo "Vulkan dependencies installed."
    fi

    read -p "Do you wan't to install WebGL dependencies now? (y/n): " install_webgl
    if [ "$install_webgl" = "y" ]; then
        echo "Installing WebGL dependencies..."
        pip install -r WhaleEngine/requirements/webGLrequirements.txt
        echo "WebGL dependencies installed."
    fi

    echo "All selected dependencies installed."
}

function install_dependencies() {
    echo "Making environment..."
    python3 -m venv .venv
    source .venv/bin/activate

    echo "Upgrading pip..."
    pip install --upgrade pip
    echo "pip upgraded."

    echo "Installing main dependencies..."
    pip install -r WhaleEngine/requirements/mainrequirements.txt
    echo "main dependencies installed."

    install_other_dependencies
}

echo "Select what you wan't to do:"
echo "1 - Install/update/reinstall WhaleEngine"
echo "2 - Reinstall or install (more) Dependencies"
echo "3 - Download documentation"
echo "4 - Make .gitignore"
echo "5 - Exit"

read -p "Select an option (1-5): " number

case "$number" in
    1)  
        echo "Removing old WhaleEngine installation if it exists..."
        rm -rf "WhaleEngine"
        echo "old WhaleEngine installation removed."
        echo "Removing old virtual environment if it exists..."
        rm -rf ".venv"
        echo "old virtual environment removed."

        echo "Cloning whale-engine..."
        git clone "$REPO" "$TEMP_DIR"
        echo "whale-engine cloned."

        echo "Copying WhaleEngine..."
        cp -r "$TEMP_DIR/WhaleEngine" .
        echo "WhaleEngine copied."

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
        echo "Clone deleted."

        echo "Done!"
        read -p "Do you wan't to install dependencies now? (y/n): " install_deps
        if [ "$install_deps" = "y" ]; then
            install_dependencies
        fi
        ;;
    2)  
        if [ ! -d ".venv" ]; then
            echo "Installing dependencies..."
            install_dependencies
            echo "Dependencies installed."
        else
            echo "Select what you wan't to do:"
            echo "1) Reinstall dependencies"
            echo "2) Install more dependencies"
            read -p "Select an option (1-2): " dep_option
            case "$dep_option" in
                1)  
                    echo "Reinstalling dependencies..."
                    echo "Deleting old virtual environment..."
                    rm -rf ".venv"
                    echo "Old virtual environment deleted."
                    echo "Reinstalling dependencies..."
                    install_dependencies
                    echo "Dependencies reinstalled."
                    ;;
                2)
                    echo "Installing more dependencies..."
                    source .venv/bin/activate
                    install_other_dependencies
                    echo "More dependencies installed."
                    ;;
                *)
                    echo "Invalid option. Please select 1 or 2."
                    ;;
            esac
        fi
        
        ;;
    3)
        echo "Downloading documentation..."
        echo "Removing old documentation if it exists..."
        rm -rf "documentations"
        echo "old documentation removed."
        
        echo "Cloning whale-engine..."
        git clone "$REPO" "$TEMP_DIR"
        echo "whale-engine cloned."
        
        echo "Creating documentation directory..."
        mkdir -p "documentations"
        echo "Documentation directory created."

        echo "Copying documentation..."
        cp -r "$TEMP_DIR/documentation.md" "documentations"
        cp -r "$TEMP_DIR/examples" "documentations"
        echo "Documentation copied."

        echo "Removing temporary directory..."
        rm -rf "$TEMP_DIR"
        echo "Temporary directory removed."

        echo "Documentation setup completed."
        ;;
    4)
        echo "Making .gitignore..."

        echo "Removing old .gitignore if it exists..."
        rm -f ".gitignore"
        echo "Old .gitignore removed."
        
        echo "Cloning whale-engine..."
        git clone "$REPO" "$TEMP_DIR"
        echo "whale-engine cloned."

        echo "Copying .gitignore..."
        cp -r "$TEMP_DIR/setup/.gitignoretemplate" ".gitignore"
        echo ".gitignore copied."

        echo "Removing temporary directory..."
        rm -rf "$TEMP_DIR"
        echo "Temporary directory removed."

        echo ".gitignore setup completed."
        ;;
    5)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid option. Please select a number between 1 and 5."
        ;;
esac

echo "Setup finished."