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
    echo "This project uses sio2jail which might not work without running:"
    echo "sysctl -w kernel.perf_event_paranoid=-1"

    echo ""
    echo "modify thus setpu to run with source"
    echo "ulimit -s unlimited"

    echo ""
    echo "To activate entry points run:"
    echo "source $VENV_DIR/bin/activate"
else
    echo "Installation failed."
    exit 1
fi