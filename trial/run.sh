#!/bin/bash
# run.sh - Simple script to start the application

echo "🤖 Starting AI Video Summarizer..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements if not already installed
echo "Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads
mkdir -p templates

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copying .env.example..."
    echo "Please edit .env with your API keys for better results."
    cp .env.example .env
fi

# Start the Flask server
echo "🚀 Starting Flask server on http://localhost:5000"
python app.py
