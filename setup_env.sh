#!/bin/bash

# BirdingPlanner Virtual Environment Setup Script
# This script helps manage the Python virtual environment for the BirdingPlanner project

set -e  # Exit on any error

echo "🦅 BirdingPlanner Environment Setup"
echo "=================================="

# Check if virtual environment exists
if [ -d "birding_env" ]; then
    echo "✅ Virtual environment 'birding_env' already exists"
else
    echo "📦 Creating virtual environment 'birding_env'..."
    python3 -m venv birding_env
    echo "✅ Virtual environment created successfully"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source birding_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing project dependencies..."
pip install -r requirements.txt

echo ""
echo "🎉 Environment setup complete!"
echo ""
echo "To activate the environment in the future, run:"
echo "  source birding_env/bin/activate"
echo ""
echo "To deactivate the environment, run:"
echo "  deactivate"
echo ""
echo "To run BirdingPlanner:"
echo "  python mcp_server/main.py"
echo ""
echo "To test advanced features:"
echo "  python test_different_species.py" 