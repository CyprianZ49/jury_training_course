#!/bin/bash

VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Make sure python3-venv is installed."
        exit 1
    fi
else
    echo "Virtual environment '$VENV_DIR' already exists. Skipping."
fi

source "$VENV_DIR/bin/activate"

pip install --upgrade pip --quiet

if pip install -e .; then
    echo ""
    echo "Run 'source $VENV_DIR/bin/activate' to start working."
else
    echo "Installation failed."
    exit 1
fi