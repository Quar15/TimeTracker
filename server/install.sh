#!/bin/bash

# Update packages and Upgrade system
echo -e "\n Updating System..."
sudo apt-get update -y && sudo apt-get upgrade -y

# Install Python3 and dependencies
sudo apt-get install python3 python3-pip
python3 -m pip install flask numpy matplotlib