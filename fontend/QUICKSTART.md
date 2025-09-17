# 🚀 LLM Ensemble Frontend - Quick Start Guide

Welcome to the LLM Ensemble Frontend! This modern React interface provides real-time visualization of your multi-perspective AI analysis system.

## ✨ What You'll Get

- **Real-time Agent Monitoring**: Watch Claude, GPT, and Grok analyze your queries live
- **Multi-Perspective Analysis**: See economic, environmental, and technological perspectives unfold
- **Beautiful Pastel UI**: Inspired by Claude, GPT, and X.AI interfaces (no purple!)
- **WebSocket Communication**: Instant updates and seamless backend integration

## 🏃‍♀️ Quick Start (2 Minutes)

### Option 1: Automated Startup
```bash
# Run the all-in-one startup script
./start_system.sh
```

### Option 2: Manual Setup
```bash
# Terminal 1: Start WebSocket Server
pip3 install websockets
python3 websocket_server.py

# Terminal 2: Start Frontend (if Node.js is available)
npm install
npm run dev
```

## 🌐 Access the Application

1. **WebSocket Server**: Starts automatically on `ws://localhost:8001`
2. **Frontend Interface**: Open `http://localhost:5173` in your browser
3. **Connection Status**: Check the header for green "Connected" indicator

## 🎯 Using the Interface

### 1. Enter Your Query
- Type your question in the main input box
- Use the example queries for inspiration
- Add universal Chain of Thought guidance if desired

### 2. Configure Perspectives (Optional)
- Click "Perspective-Specific Chain of Thought" to expand
- Add specific guidance for economic, environmental, and technological analysis
- Each perspective gets tailored instructions

### 3. Start Analysis
- Click "Start Multi-Perspective Analysis"
- Watch the real-time progress tracker
- Monitor each agent's status and output

### 4. View Results
- See the final synthesis and judge evaluation
- Check quality scores and performance metrics
- Export results for further use

## 🎨 Interface Features

### Header
- **Connection Status**: Real-time WebSocket connection indicator
- **Model Badges**: Shows available AI models (Claude, GPT, Grok)
- **Clean Design**: Pastel colors with no purple theme

### Query Input
- **Smart Examples**: Pre-loaded example queries
- **Universal CoT**: General guidance for all models
- **Perspective CoT**: Specific instructions per analysis dimension
- **Responsive Design**: Works on all screen sizes

### Real-time Display
- **Progress Tracker**: 6-step visual pipeline
- **Agent Grid**: Live status cards for each AI model
- **Perspective Evolution**: Watch analysis grow from baseline to complete
- **Confidence Tracking**: Real-time confidence scores

### Results Section
- **Final Synthesis**: Comprehensive multi-perspective conclusion
- **Judge Analysis**: Independent evaluation and quality assessment
- **Performance Metrics**: Improvement over baseline analysis
- **Quality Scores**: Individual model performance ratings

## 🔧 Troubleshooting

### WebSocket Connection Issues
```bash
# Check if server is running
ps aux | grep websocket_server

# Restart WebSocket server
python3 websocket_server.py
```

### Frontend Issues
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Connection Status
- **Green "Connected"**: System ready for analysis
- **Yellow "Connecting"**: Attempting to establish connection
- **Red "Disconnected"**: Check WebSocket server status

## 📱 Mobile Support

The interface is fully responsive and works on:
- **Desktop**: Full feature set with multi-column layout
- **Tablet**: Adaptive layout with touch-friendly controls
- **Mobile**: Optimized single-column view with core functionality

## 🎨 Design Philosophy

### Color Palette
- **Claude Green**: Soft green backgrounds with vibrant green accents
- **GPT Blue**: Light blue backgrounds with modern blue accents
- **X.AI Orange**: Warm peach backgrounds with orange highlights
- **No Purple**: Deliberately avoided to create a unique aesthetic

### UI Principles
- **Pastel Softness**: Gentle colors that reduce eye strain
- **Real-time Feedback**: Immediate visual response to user actions
- **Progressive Disclosure**: Advanced features hidden until needed
- **Mobile-First**: Responsive design starting from mobile up

## 🔗 Backend Integration

### Current Setup
- **Demo Mode**: WebSocket server provides realistic demo analysis
- **Real-time Updates**: Simulates actual LLM Ensemble workflow
- **Complete Pipeline**: Shows all 6 steps of multi-perspective analysis

### Production Integration
- Replace demo analysis with actual LLM Ensemble backend calls
- Connect to existing multi_perspective_main.py system
- Maintain WebSocket communication for real-time updates

## 📊 Example Analysis Flow

1. **Query**: "What are the benefits of renewable energy?"
2. **Universal CoT**: "be concise, focus on evidence-based analysis"
3. **Economic CoT**: "analyze costs and market impacts"
4. **Environmental CoT**: "consider climate and sustainability effects"
5. **Technological CoT**: "evaluate technical feasibility and innovation"

Watch as:
- Each agent generates baseline responses
- Economic perspective analysis unfolds
- Environmental considerations are added
- Technological feasibility is evaluated
- Judge synthesizes all perspectives
- Final comprehensive analysis is presented

## 🚀 Next Steps

1. **Try Different Queries**: Test various topics and perspectives
2. **Experiment with CoT**: See how different guidance affects analysis
3. **Monitor Performance**: Watch quality scores and improvement metrics
4. **Mobile Testing**: Try the interface on different devices
5. **Backend Integration**: Connect to your actual LLM Ensemble system

## 🤝 Support

- **Documentation**: See README.md for technical details
- **Issues**: Check console for error messages
- **Performance**: Monitor network tab for WebSocket communication
- **Customization**: Modify CSS variables for different color schemes

---

**Enjoy your multi-perspective AI analysis! 🧠✨**
