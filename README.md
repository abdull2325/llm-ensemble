# Enhanced Multi-Perspective LLM Ensemble System

A sophisticated LangGraph-based LLM ensemble system that combines Claude, GPT, and X.AI Grok models for comprehensive multi-perspective analysis with advanced Chain of Thought capabilities.

## 🎯 Key Features

### Multi-Perspective Analysis Framework
- **Economic Perspective**: Cost analysis, market impacts, investment considerations
- **Environmental Perspective**: Climate effects, sustainability, ecosystem impacts  
- **Technological Perspective**: Innovation potential, limitations, mitigation strategies

### Advanced Chain of Thought Integration
- **Universal CoT**: Consistent analytical guidance across all models
- **Perspective-Specific CoT**: Tailored instructions for each analytical dimension
- **Progressive Enhancement**: Multi-step analysis building upon previous insights

### Performance Optimization
- **Baseline Comparison**: Measures improvement over raw model responses
- **Real-time Metrics**: Processing time, quality scores, confidence tracking
- **Memory Persistence**: Learning from historical analysis patterns

## 🏗️ System Architecture

Built on **LangGraph 0.2.34** for robust workflow orchestration:

```
Multi-Perspective Analysis Pipeline:
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Baseline        │    │ Step 1: Economic │    │ Step 2: Eco +   │
│ Generation      │ -> │ Perspective      │ -> │ Environmental   │
│ (No Guidance)   │    │ Analysis         │    │ Analysis        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Performance     │ <- │ Judge Evaluation │ <- │ Step 3: Complete│
│ Logging &       │    │ & Synthesis      │    │ 3-Perspective   │
│ Comparison      │    │                  │    │ Analysis        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd llm_ensemble_langgraph

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### API Configuration
Set up your API keys in `config/settings.py`:
```python
CLAUDE_API_KEY = "your-claude-key"
OPENAI_API_KEY = "your-openai-key"  
XAI_API_KEY = "your-xai-key"
```

### Basic Usage

#### Simple Multi-Perspective Analysis
```python
from multi_perspective_main import EnhancedLLMEnsembleSystem

ensemble = EnhancedLLMEnsembleSystem()
result = await ensemble.process_multi_perspective_query(
    query="What are the benefits of renewable energy?",
    universal_cot="be concise, focus on evidence-based analysis",
    chain_of_thought_1="consider economic costs and benefits",
    chain_of_thought_2="consider environmental impacts",
    chain_of_thought_3="consider technological capabilities"
)
```

#### Command Line Interface
```bash
# Basic query
python multi_perspective_main.py "Your question here"

# With Chain of Thought guidance
python multi_perspective_main.py "Your question here" 
  --universal_cot "be specific and factual" 
  --cot1 "focus on economic aspects" 
  --cot2 "focus on environmental aspects" 
  --cot3 "focus on technological aspects"
```

#### Comprehensive Demo
```bash
# Run the full demonstration
python multi_perspective_demo.py
```

## 📊 Performance Results

### Demo Test Results
- **Processing Time**: 40-48 seconds per multi-perspective query
- **Performance Improvement**: 1.36x - 1.45x over baseline responses
- **Completion Rate**: 100% (6/6 steps completed consistently)
- **Quality Enhancement**: Measurable improvements in comprehensiveness and specificity

### Chain of Thought Benefits
- More focused and relevant responses
- Better perspective alignment across models
- Enhanced analytical depth and synthesis quality
- Consistent reasoning patterns across different queries

## 🔧 Advanced Configuration

### Custom Perspectives
```python
# Modify perspectives in multi_perspective_state.py
class Perspective(str, Enum):
    ECONOMIC = "economic"
    ENVIRONMENTAL = "environmental" 
    TECHNOLOGICAL = "technological"
    # Add custom perspectives here
```

### Enhanced CoT Prompting
```python
# Example perspective-specific CoT configurations
cot_configs = {
    "economic": "analyze costs, ROI, market dynamics over 10-year horizon",
    "environmental": "assess carbon footprint, resource usage, sustainability metrics",
    "technological": "evaluate innovation potential, scalability, technical limitations"
}
```

## 📁 Project Structure

```
/llm_ensemble_langgraph/
├── config/                    # Configuration and API keys
├── graph/                     # LangGraph workflow definitions
│   ├── multi_perspective_*    # Enhanced multi-perspective system
│   └── ensemble_*             # Original ensemble system
├── models/                    # LLM API integrations
├── utils/                     # Utilities (CoT, judge, memory)
├── multi_perspective_main.py  # Enhanced main entry point
├── multi_perspective_demo.py  # Comprehensive demo
└── PROJECT_SUMMARY.md         # Detailed implementation summary
```

## 🔍 System Capabilities

### Multi-Step Analysis Process
1. **Baseline Generation**: Raw responses without guidance
2. **Economic Analysis**: Cost-benefit perspective with CoT
3. **Environmental Integration**: Sustainability considerations
4. **Technological Synthesis**: Innovation and feasibility analysis
5. **Judge Evaluation**: Independent assessment and synthesis
6. **Performance Logging**: Metrics and improvement tracking

### Quality Assurance
- Input validation and error handling
- API failure graceful degradation
- Response quality scoring
- Performance comparison metrics

## 🎯 Use Cases

### Research and Analysis
- Policy impact assessment across multiple dimensions
- Technology evaluation with comprehensive perspective analysis
- Market research with economic, environmental, and technical insights

### Decision Support
- Strategic planning with multi-perspective consideration
- Risk assessment across different analytical frameworks
- Innovation evaluation with holistic analysis

### Educational Applications
- Teaching critical thinking through perspective analysis
- Demonstrating complex problem-solving approaches
- Comparative analysis methodology

## 📈 Performance Monitoring

The system includes comprehensive performance tracking:
- Processing time optimization
- Quality score aggregation  
- Baseline vs ensemble improvement metrics
- Memory-based learning and pattern recognition

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement enhancements with proper testing
4. Submit a pull request with detailed description

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with LangGraph for robust workflow orchestration
- Integrates Claude, GPT, and X.AI Grok for diverse AI perspectives
- Implements advanced Chain of Thought methodologies
- Designed for production-ready multi-perspective analysis
