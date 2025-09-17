#!/bin/bash
# Multi-Perspective LLM Ensemble System Launcher (Shell Script Version)
# Alternative to the Python launcher for simpler execution

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project paths
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"
BACKEND_SCRIPT="$PROJECT_ROOT/backend_websocket_server.py"
FRONTEND_DIR="$PROJECT_ROOT/fontend"

# Function to print colored output
print_colored() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to cleanup processes on exit
cleanup() {
    print_colored $YELLOW "\n Shutting down services..."
    
    if [[ ! -z "$BACKEND_PID" ]]; then
        kill $BACKEND_PID 2>/dev/null
        print_colored $GREEN " Backend server stopped"
    fi
    
    if [[ ! -z "$FRONTEND_PID" ]]; then
        kill $FRONTEND_PID 2>/dev/null
        print_colored $GREEN " Frontend server stopped"
    fi
    
    print_colored $BLUE " System shutdown complete"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Validate paths
validate_setup() {
    print_colored $BLUE " Validating system setup..."
    
    if [[ ! -f "$VENV_PYTHON" ]]; then
        print_colored $RED " Virtual environment not found. Please create it first:"
        echo "   python -m venv .venv"
        echo "   source .venv/bin/activate"
        echo "   pip install -r requirements.txt"
        exit 1
    fi
    
    if [[ ! -f "$BACKEND_SCRIPT" ]]; then
        print_colored $RED " Backend script not found at: $BACKEND_SCRIPT"
        exit 1
    fi
    
    if [[ ! -d "$FRONTEND_DIR" ]]; then
        print_colored $RED " Frontend directory not found at: $FRONTEND_DIR"
        exit 1
    fi
    
    if [[ ! -f "$FRONTEND_DIR/package.json" ]]; then
        print_colored $RED "Frontend package.json not found. Please run 'npm install' in the frontend directory."
        exit 1
    fi
    
    print_colored $GREEN " System setup validation complete"
}

# Start backend server
start_backend() {
    print_colored $BLUE " Starting Backend WebSocket Server..."
    
    cd "$PROJECT_ROOT"
    "$VENV_PYTHON" "$BACKEND_SCRIPT" &
    BACKEND_PID=$!
    
    # Wait a moment for backend to start
    sleep 3
    
    # Check if backend is still running
    if kill -0 $BACKEND_PID 2>/dev/null; then
        print_colored $GREEN " Backend server started successfully (PID: $BACKEND_PID)"
        return 0
    else
        print_colored $RED " Backend server failed to start"
        return 1
    fi
}

# Start frontend server
start_frontend() {
    print_colored $BLUE " Starting Frontend Development Server..."
    
    cd "$FRONTEND_DIR"
    
    # Check if node_modules exists
    if [[ ! -d "node_modules" ]]; then
        print_colored $YELLOW " Installing frontend dependencies..."
        npm install
        if [[ $? -ne 0 ]]; then
            print_colored $RED " Failed to install frontend dependencies"
            return 1
        fi
        print_colored $GREEN " Frontend dependencies installed"
    fi
    
    npm run dev &
    FRONTEND_PID=$!
    
    # Wait a moment for frontend to start
    sleep 5
    
    # Check if frontend is still running
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        print_colored $GREEN " Frontend server started successfully (PID: $FRONTEND_PID)"
        return 0
    else
        print_colored $RED " Frontend server failed to start"
        return 1
    fi
}

# Main execution
main() {
    echo "================================================================================"
    print_colored $BLUE " Multi-Perspective LLM Ensemble System Launcher"
    echo "================================================================================"
    print_colored $YELLOW " Project root: $PROJECT_ROOT"
    print_colored $YELLOW " Python virtual env: $VENV_PYTHON"
    print_colored $YELLOW " Backend script: $BACKEND_SCRIPT"
    print_colored $YELLOW " Frontend directory: $FRONTEND_DIR"
    echo "================================================================================"
    
    # Validate setup
    validate_setup
    
    # Start backend
    if ! start_backend; then
        print_colored $RED " Failed to start backend. Exiting."
        exit 1
    fi
    
    # Start frontend
    if ! start_frontend; then
        print_colored $RED " Failed to start frontend. Stopping backend and exiting."
        cleanup
        exit 1
    fi
    
    echo ""
    echo "================================================================================"
    print_colored $GREEN " SYSTEM SUCCESSFULLY STARTED!"
    echo "================================================================================"
    print_colored $BLUE " Backend WebSocket Server: ws://localhost:8001"
    print_colored $BLUE " Frontend Application: http://localhost:5173"
    print_colored $BLUE " Multi-Perspective Analysis: Economic, Environmental, Technological"
    print_colored $BLUE " Chain of Thought: Universal + Perspective-specific"
    echo "================================================================================"
    print_colored $YELLOW " Features Available:"
    print_colored $YELLOW "   • Real-time agent output visualization"
    print_colored $YELLOW "   • Multi-step perspective analysis"
    print_colored $YELLOW "   • Baseline vs ensemble comparison"
    print_colored $YELLOW "   • Live progress tracking"
    print_colored $YELLOW "   • Performance metrics"
    echo "================================================================================"
    print_colored $GREEN " Press Ctrl+C to stop both services"
    print_colored $GREEN " Open your browser to http://localhost:5173 to use the application"
    echo "================================================================================"
    
    # Keep script running and monitor processes
    while true; do
        # Check if backend is still running
        if ! kill -0 $BACKEND_PID 2>/dev/null; then
            print_colored $RED " Backend process has stopped unexpectedly"
            break
        fi
        
        # Check if frontend is still running
        if ! kill -0 $FRONTEND_PID 2>/dev/null; then
            print_colored $RED " Frontend process has stopped unexpectedly"
            break
        fi
        
        sleep 2
    done
    
    cleanup
}

# Run main function
main "$@"
