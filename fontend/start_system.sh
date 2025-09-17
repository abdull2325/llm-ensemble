#!/bin/bash

# LLM Ensemble Frontend Startup Script
echo "🚀 LLM Ensemble Frontend & WebSocket Server Startup"
echo "=================================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.9+ and try again."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install WebSocket server dependencies
echo "📦 Installing WebSocket server dependencies..."
if pip3 install -r backend_requirements.txt; then
    echo "✅ WebSocket dependencies installed"
else
    echo "⚠️  Could not install WebSocket dependencies. Trying to continue..."
fi

# Check if Node.js is available
if command -v node &> /dev/null; then
    echo "✅ Node.js found: $(node --version)"
    
    # Install frontend dependencies if package.json exists and node_modules doesn't
    if [ -f "package.json" ] && [ ! -d "node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        if npm install; then
            echo "✅ Frontend dependencies installed"
        else
            echo "❌ Failed to install frontend dependencies"
        fi
    fi
else
    echo "⚠️  Node.js not found. Frontend will need to be set up manually."
    echo "   Install Node.js 18+ and run: npm install && npm run dev"
fi

echo ""
echo "🎯 Starting WebSocket Server..."
echo "   Server will run on: ws://localhost:8001"
echo "   Use Ctrl+C to stop"
echo ""
echo "📝 Next steps:"
echo "   1. Keep this terminal open (WebSocket server)"
echo "   2. Open a new terminal"
echo "   3. Run: npm run dev"
echo "   4. Open browser to: http://localhost:5173"
echo ""

# Start the WebSocket server
python3 websocket_server.py
