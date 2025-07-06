#!/bin/bash
echo "Uninstalling ShiftLock"
echo "---------------------"
sudo make uninstall
sudo mandb -q
echo "Uninstall complete"