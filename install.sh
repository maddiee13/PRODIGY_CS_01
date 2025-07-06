#!/bin/bash
echo "Installing ShiftLock for Debian/Ubuntu"
echo "-------------------------------------"

# Install dependencies
sudo apt update
sudo apt install -y python3 python3-venv

# Install ShiftLock
sudo make install

# Set up man database
sudo mandb -q

echo ""
echo "ShiftLock installation complete!"
echo "Try: shiftlock encrypt -t 'Hello World' -s 5"