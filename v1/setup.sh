#!/bin/bash

# if this file fails to run with error:
# 		permission denied: ./setup.sh
# run the following command
# 		chmod u+x setup.sh

# Check if pip is installed
if ! command -v pip &> /dev/null
then
	echo "pip could not be found. Please install Python and pip."
	exit 1
fi

# Install required packages
pip install -r requirements.txt

echo "All dependencies have been installed successfully."