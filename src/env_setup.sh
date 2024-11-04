#!/bin/bash

# Step 1: Create a virtual environment in the "venv" directory
python3 -m venv venv

# Step 2: Activate the virtual environment
source venv/bin/activate

# Step 3: Install packages from requirements.txt
pip install -r requirements.txt

echo "Environment setup complete. Virtual environment is activated."
