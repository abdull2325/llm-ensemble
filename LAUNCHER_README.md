# System Launcher Scripts

This directory contains two launcher scripts to start both the backend and frontend of the Multi-Perspective LLM Ensemble System simultaneously.

## Available Launchers

### 1. Python Launcher (Recommended)
```bash
python start_system.py
```
**Features:**
- ✅ Advanced process management
- ✅ Real-time output monitoring with prefixes
- ✅ Automatic dependency checking
- ✅ Graceful shutdown handling
- ✅ Cross-platform compatibility
- ✅ Colored output and status messages

### 2. Shell Script Launcher (Alternative)
```bash
./start_system.sh
```
**Features:**
- ✅ Fast startup with minimal overhead
- ✅ Colored terminal output
- ✅ Process monitoring
- ✅ Signal handling for clean shutdown
- ✅ Native bash performance
- ⚠️ Unix/Linux/macOS only

## What the Launchers Do

1. **Validation**: Check that all required files and dependencies exist
2. **Backend Startup**: Start the WebSocket server on `ws://localhost:8001`
3. **Frontend Startup**: Start the Vite development server on `http://localhost:5173`
4. **Monitoring**: Monitor both processes and restart if needed
5. **Cleanup**: Gracefully shutdown both services on Ctrl+C

## System Requirements

### Backend Requirements
- Python 3.8+ with virtual environment at `.venv/`
- All Python dependencies installed (`pip install -r requirements.txt`)
- Valid API keys configured in `config/settings.py`

### Frontend Requirements
- Node.js 16+ and npm
- Frontend dependencies installed (`npm install` in `fontend/` directory)

## Usage Examples

### Quick Start (Python)
```bash
# Make sure you're in the project root
cd /path/to/llm_ensemble_langgraph

# Start both services
python start_system.py
```

### Quick Start (Shell)
```bash
# Make sure you're in the project root
cd /path/to/llm_ensemble_langgraph

# Start both services
./start_system.sh
```

### Expected Output
```
================================================================================
🚀 Multi-Perspective LLM Ensemble System Launcher
================================================================================
📁 Project root: /path/to/llm_ensemble_langgraph
🐍 Python virtual env: /path/to/.venv/bin/python
🔧 Backend script: /path/to/backend_websocket_server.py
🌐 Frontend directory: /path/to/fontend
================================================================================
🚀 Starting Backend WebSocket Server...
✅ Backend server started successfully
🎨 Starting Frontend Development Server...
✅ Frontend server started successfully

================================================================================
🎉 SYSTEM SUCCESSFULLY STARTED!
================================================================================
🔧 Backend WebSocket Server: ws://localhost:8001
🌐 Frontend Application: http://localhost:5173
📊 Multi-Perspective Analysis: Economic, Environmental, Technological
🧠 Chain of Thought: Universal + Perspective-specific
================================================================================
⚡ Press Ctrl+C to stop both services
🌐 Open your browser to http://localhost:5173 to use the application
================================================================================
```

## Troubleshooting

### Common Issues

1. **Virtual Environment Not Found**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Frontend Dependencies Missing**
   ```bash
   cd fontend/
   npm install
   ```

3. **API Keys Not Configured**
   - Edit `config/settings.py`
   - Add your Claude, OpenAI, and X.AI API keys

4. **Port Already in Use**
   - Backend: Check if port 8001 is available
   - Frontend: Check if port 5173 is available
   - Kill existing processes: `lsof -ti:8001 | xargs kill -9`

### Manual Startup (If Launchers Fail)

**Terminal 1 - Backend:**
```bash
cd /path/to/llm_ensemble_langgraph
source .venv/bin/activate
python backend_websocket_server.py
```

**Terminal 2 - Frontend:**
```bash
cd /path/to/llm_ensemble_langgraph/fontend
npm run dev
```

## System Architecture

The launchers coordinate these components:

```
┌─────────────────────────────────────────────────────────────┐
│                    System Launcher                          │
│  (start_system.py or start_system.sh)                      │
└─────────────┬─────────────────────────┬─────────────────────┘
              │                         │
              ▼                         ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│   Backend WebSocket     │   │   Frontend Vite Dev     │
│   Server (Port 8001)    │   │   Server (Port 5173)    │
│                         │   │                         │
│ • LangGraph Workflow    │   │ • React + TypeScript    │
│ • Multi-Perspective     │   │ • Real-time WebSocket   │
│ • Chain of Thought      │   │ • Agent Visualization   │
│ • Claude/GPT/Grok APIs  │   │ • Progress Tracking     │
└─────────────────────────┘   └─────────────────────────┘
```

## Next Steps

After starting the system:

1. Open your browser to `http://localhost:5173`
2. Enter a query in the input field
3. Optionally configure Chain of Thought instructions
4. Click "Analyze" to start the multi-perspective analysis
5. Watch real-time agent outputs and progress
6. Review the comprehensive synthesis and performance metrics

The system will provide:
- Economic perspective analysis
- Environmental perspective analysis  
- Technological perspective analysis
- Baseline comparison
- Judge evaluation and synthesis
- Performance improvement metrics
