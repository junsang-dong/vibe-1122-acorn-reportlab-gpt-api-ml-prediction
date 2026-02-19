#!/bin/bash

echo "==================================================="
echo "🚀 Sales Report Generator - Quick Start Script"
echo "==================================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    echo "   Visit: https://www.python.org/"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ Python version: $(python3 --version)"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
    echo ""
fi

# Check if Python packages are installed
echo "📦 Checking Python dependencies..."
if ! python3 -c "import pandas" &> /dev/null; then
    echo "📦 Installing Python dependencies..."
    pip3 install -r requirements.txt
    echo ""
else
    echo "✅ Python dependencies are already installed"
    echo ""
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from example..."
    cp .env.example .env 2>/dev/null || echo "OPENAI_API_KEY=your_openai_api_key_here
PORT=8080" > .env
    echo "✅ .env file created"
    echo "⚠️  Please edit .env and add your OpenAI API key"
    echo "📌 Server will run on http://localhost:8080"
    echo ""
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads output temp_charts
echo "✅ Directories created"
echo ""

# Start the server
echo "==================================================="
echo "🎉 Starting the server..."
echo "==================================================="
echo ""

npm start

