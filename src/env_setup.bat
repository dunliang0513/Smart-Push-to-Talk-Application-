@echo off

:: Step 1: Create a virtual environment in the "venv" directory
python -m venv venv

:: Step 2: Activate the virtual environment
call venv\Scripts\activate

:: Step 3: Install packages from requirements.txt
pip install -r requirements.txt

echo Environment setup complete. Virtual environment is activated.
