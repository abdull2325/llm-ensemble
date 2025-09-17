# LLM Ensemble Frontend

A modern React TypeScript frontend for the Multi-Perspective LLM Ensemble System with real-time agent output display.

## 🎨 Design Features

### Visual Design
- **Pastel Color Palette**: Inspired by Claude, GPT, and X.AI interfaces
- **No Purple**: Uses soft greens, blues, and oranges instead
- **Modern UI**: Clean, minimalist design with subtle shadows and animations
- **Responsive**: Works on desktop, tablet, and mobile devices

### Real-time Features
- **Live Agent Monitoring**: Watch Claude, GPT, and Grok work in real-time
- **Step-by-Step Progress**: Visual progress tracker through all analysis phases
- **WebSocket Communication**: Instant updates from backend to frontend
- **Perspective Analysis**: See economic, environmental, and technological perspectives unfold

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.9+ (for WebSocket server)

### 1. Start the WebSocket Server
```bash
# Install Python dependencies
pip install -r backend_requirements.txt

# Start the WebSocket server
python websocket_server.py
```

The server will start on `ws://localhost:8001`

### 2. Start the Frontend
```bash
# Install dependencies (when Node.js is available)
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 🏗️ Architecture

### Frontend Stack
- **React 18** with TypeScript
- **Vite** for fast development and building
- **WebSocket** for real-time communication
- **CSS Variables** for consistent theming
- **Responsive Design** with CSS Grid and Flexbox

### Backend Integration
- **WebSocket Server**: Python-based real-time communication bridge
- **LLM Ensemble Connection**: Direct integration with the multi-perspective system
- **Real-time Updates**: Live streaming of analysis progress and results

## 🎯 Features

### Query Interface
- **Smart Input**: Large, user-friendly query input with examples
- **Universal CoT**: General Chain of Thought guidance for all models
- **Perspective-Specific CoT**: Tailored instructions for each analysis dimension
- **Example Queries**: Pre-loaded examples for quick testing

### Real-time Analysis Display
- **Progress Tracker**: 6-step visual progress through the analysis pipeline
- **Agent Grid**: Live status and output from Claude, GPT, Grok, and Judge
- **Perspective Evolution**: Watch analysis evolve from baseline through all perspectives
- **Confidence Tracking**: Real-time confidence scores for each agent

### Results Presentation
- **Final Synthesis**: Comprehensive multi-perspective conclusion
- **Judge Analysis**: Independent evaluation and quality assessment
- **Performance Metrics**: Improvement over baseline, quality scores
- **Export Capability**: Save and share analysis results

## 🎨 Color Scheme

### Primary Colors
- **Claude Green**: `#e8f5e8` (background), `#4ade80` (accent)
- **GPT Blue**: `#e6f3ff` (background), `#60a5fa` (accent)
- **X.AI Orange**: `#fef3e2` (background), `#fb923c` (accent)

### Neutral Pastels
- **Soft Gray**: `#f1f5f9`
- **Warm White**: `#fefefe`
- **Light Blue**: `#f0f9ff`
- **Mint Green**: `#f0fdfa`
- **Peach**: `#fef7ed`

## 🔧 Development

### Project Structure
```
src/
├── components/          # React components
│   ├── Header.tsx      # Main header with connection status
│   ├── QueryInput.tsx  # Query input with CoT configuration
│   ├── AgentGrid.tsx   # Real-time agent display
│   ├── ProgressTracker.tsx  # Step-by-step progress
│   └── Results.tsx     # Final results display
├── hooks/
│   └── useWebSocket.ts # WebSocket connection hook
├── types.ts            # TypeScript type definitions
├── App.tsx             # Main application component
├── App.css             # Application styles
└── index.css           # Global styles and variables
```

### Component Architecture
- **Modular Components**: Each feature is a self-contained component
- **TypeScript**: Full type safety throughout the application
- **Custom Hooks**: Reusable logic for WebSocket communication
- **CSS Variables**: Consistent theming and easy customization

## 🌐 WebSocket API

### Message Types

#### Frontend → Backend
```typescript
// Start analysis
{
  "type": "start_analysis",
  "query": "Your question here",
  "universalCot": "General guidance",
  "perspectiveCots": {
    "economic": "Economic guidance",
    "environmental": "Environmental guidance", 
    "technological": "Technological guidance"
  }
}
```

#### Backend → Frontend
```typescript
// Analysis started
{
  "type": "analysis_started",
  "query": "Your question..."
}

// Agent update
{
  "type": "agent_update",
  "agent": "claude|gpt|grok|judge",
  "status": "thinking|processing|completed",
  "perspective": "baseline|economic|environmental|technological|synthesis",
  "output": "Current analysis text...",
  "confidence": 0.85
}

// Step completion
{
  "type": "step_complete",
  "step": 1-6
}

// Final results
{
  "type": "analysis_complete",
  "results": { /* Complete analysis results */ },
  "processing_time": 15.7
}
```

## 📱 Mobile Responsiveness

- **Adaptive Layout**: Components reorganize for smaller screens
- **Touch-Friendly**: Large buttons and touch targets
- **Optimized Performance**: Efficient rendering for mobile devices
- **Progressive Enhancement**: Core functionality works on all devices

## 🔗 Integration with LLM Ensemble Backend

The frontend is designed to integrate seamlessly with the existing LLM Ensemble backend:

1. **WebSocket Bridge**: The `websocket_server.py` acts as a bridge between frontend and backend
2. **Real-time Updates**: Live streaming of analysis progress from the LangGraph workflow
3. **Complete Integration**: Full access to multi-perspective analysis capabilities
4. **Error Handling**: Graceful degradation when backend services are unavailable

## 🚀 Deployment

### Development
```bash
npm run dev     # Start development server
npm run build   # Build for production
npm run preview # Preview production build
```

### Production
```bash
npm run build
# Deploy the `dist/` folder to your web server
# Ensure WebSocket server is running and accessible
```

## 🤝 Contributing

1. Follow the existing code style and TypeScript patterns
2. Test real-time features with the WebSocket server
3. Ensure mobile responsiveness for new components
4. Maintain the pastel color scheme and design consistency

## 📄 License

MIT License - Same as the main LLM Ensemble project
