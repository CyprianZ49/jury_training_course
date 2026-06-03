#!/bin/bash

VENV_DIR=".venv"

CURRENT_PERF=$(sysctl -n kernel.perf_event_paranoid 2>/dev/null)
if [ "$CURRENT_PERF" != "-1" ]; then
    echo "This project uses sio2jail which requires kernel.perf_event_paranoid=-1."
    sudo sysctl -w kernel.perf_event_paranoid=-1
else
    echo "kernel.perf_event_paranoid is set correctly."
fi

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Make sure python3-venv is installed."
        return 1 2>/dev/null || exit 1
    fi
else
    echo "Virtual environment '$VENV_DIR' already exists. Skipping."
fi

source "$VENV_DIR/bin/activate"

ulimit -s unlimited

pip install --upgrade pip --quiet

if pip install -e .; then
    echo ""
    echo "Setup complete!"
else
    echo "Installation failed."
    return 1 2>/dev/null || exit 1
fi