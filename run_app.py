#!/usr/bin/env python3
"""
Launcher script for the NatureConnect application.
This script checks dependencies and launches the Streamlit app.
"""

import os
import sys
import subprocess
import importlib.util
import platform

def check_python_version():
    """Check if Python version is compatible"""
    required_version = (3, 7)  # Minimum required Python version
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"Error: Python {required_version[0]}.{required_version[1]} or higher is required.")
        print(f"Current version: {current_version[0]}.{current_version[1]}")
        return False
    
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = ['streamlit', 'pandas', 'numpy', 'matplotlib', 'plotly', 'requests', 'pillow']
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("Error: The following required packages are missing:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nPlease install them using:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def check_data_directory():
    """Ensure data directory exists and has sample data"""
    # Check if data directory exists
    if not os.path.exists('data'):
        print("Creating data directory...")
        os.makedirs('data')
    
    # Check for sample data
    sample_files = ['sample_trails.csv', 'sample_events.csv']
    for file in sample_files:
        if not os.path.exists(os.path.join('data', file)):
            # Sample data will be created by the app, so just notify
            print(f"Note: Sample data file '{file}' not found. It will be created when the app runs.")
    
    return True

def launch_app():
    """Launch the Streamlit app"""
    try:
        print("Launching NatureConnect application...")
        # Clear terminal screen before launching
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
            
        # Launch Streamlit
        subprocess.run(['streamlit', 'run', 'app.py'])
        return True
    except Exception as e:
        print(f"Error launching application: {e}")
        return False

def main():
    """Main function to run all checks and launch the app"""
    print("Preparing to launch NatureConnect...")
    print("Performing system checks...")
    
    checks = [
        (check_python_version, "Python version check"),
        (check_dependencies, "Dependencies check"),
        (check_data_directory, "Data directory check")
    ]
    
    all_passed = True
    for check_func, check_name in checks:
        print(f"Running {check_name}...", end="")
        if check_func():
            print(" PASSED")
        else:
            print(" FAILED")
            all_passed = False
            break
    
    if all_passed:
        launch_app()
        return 0
    else:
        print("\nOne or more checks failed. Please resolve the issues and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
