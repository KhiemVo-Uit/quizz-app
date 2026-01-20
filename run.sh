#!/bin/bash

# Quiz App Runner Script
# This script checks for Python, installs dependencies, and runs the application

echo "🚀 Starting Quiz Application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher to run this application."
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python3 -c "import ttkbootstrap" &> /dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "🎯 Launching Quiz Application..."
echo ""

# Run the application
python3 main.py

# Deactivate virtual environment when done
deactivate
