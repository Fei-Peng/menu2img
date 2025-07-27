#!/bin/bash

# Start the Menu2Img web application
echo "Starting Menu2Img Web Application..."
echo "Make sure you have set your OPENAI_API_KEY environment variable"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if requirements are installed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing Python dependencies..."
pip install -r src/shared/requirements.txt

# Start the web app
echo "Starting Flask web server..."
echo "Web app will be available at: http://localhost:5051"
echo "Press Ctrl+C to stop the server"
echo ""

cd src/web
python app.py 