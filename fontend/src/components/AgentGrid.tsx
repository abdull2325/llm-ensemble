import { AnalysisState, BaselineResponse, MultiPerspectiveAnalysis } from '../types';

interface AgentGridProps {
  agents: AnalysisState['agents'];
  currentStep: number;
  baselineResponses?: Record<string, BaselineResponse>;
  multiPerspectiveAnalyses?: Record<string, MultiPerspectiveAnalysis>;
}

const AgentGrid = ({ agents, currentStep, baselineResponses = {}, multiPerspectiveAnalyses = {} }: AgentGridProps) => {
  const getAgentColor = (agentName: string) => {
    const colors = {
      claude: '#ff6b35',
      gpt: '#4ecdc4', 
      grok: '#45b7d1',
      judge: '#96ceb4'
    };
    return colors[agentName as keyof typeof colors] || '#666';
  };

  const formatPerspectiveEvolution = (analysis: MultiPerspectiveAnalysis) => {
    const steps = [];
    if (analysis.step1_economic) steps.push('Economic');
    if (analysis.step2_economic_environmental) steps.push('Eco+Env');
    if (analysis.step3_complete_synthesis) steps.push('Tech+Synthesis');
    return steps.join(' → ');
  };

  return (
    <div className="agent-grid">
      <h3>Real-time Agent Analysis - Step {currentStep}</h3>
      <div className="agents">
        {Object.entries(agents).map(([name, agent]) => {
          const baseline = baselineResponses[name];
          const multiPerspective = multiPerspectiveAnalyses[name];
          const agentColor = getAgentColor(name);
          
          return (
            <div key={name} className={`agent-card ${agent.status}`} style={{ borderLeftColor: agentColor }}>
              <div className="agent-header">
                <h4 style={{ color: agentColor }}>{name.toUpperCase()}</h4>
                <div className="status-indicators">
                  <span className={`status ${agent.status}`}>{agent.status}</span>
                  {agent.cotGuidance && <span className="cot-indicator">CoT Applied</span>}
                  {name === 'judge' && <span className="judge-indicator">Judge Assessment</span>}
                </div>
              </div>
              
              <div className="agent-perspective">
                Current: {agent.perspective}
                {agent.step && <span className="step-indicator">Step {agent.step}</span>}
              </div>

              {/* Baseline Response Section */}
              {baseline && (
                <div className="baseline-section">
                  <h5>Baseline Response</h5>
                  <div className="baseline-content">
                    {baseline.content.substring(0, 150)}
                    {baseline.content.length > 150 ? '...' : ''}
                  </div>
                  <div className="baseline-meta">
                    <span>Confidence: {(baseline.confidence * 100).toFixed(0)}%</span>
                    <span>{baseline.timestamp}</span>
                  </div>
                </div>
              )}

              {/* Multi-Perspective Analysis Section */}
              {multiPerspective && (
                <div className="multi-perspective-section">
                  <h5>Multi-Perspective Evolution</h5>
                  <div className="perspective-evolution">
                    {formatPerspectiveEvolution(multiPerspective)}
                  </div>
                  {multiPerspective.final_confidence && (
                    <div className="final-confidence">
                      Final Confidence: {(multiPerspective.final_confidence * 100).toFixed(0)}%
                    </div>
                  )}
                  {multiPerspective.reasoning_evolution && multiPerspective.reasoning_evolution.length > 0 && (
                    <div className="reasoning-steps">
                      <span className="steps-count">
                        {multiPerspective.reasoning_evolution.length} reasoning steps
                      </span>
                    </div>
                  )}
                </div>
              )}

              {/* Current Output */}
              {agent.output && (
                <div className="agent-output">
                  <h5>Current Output</h5>
                  <div className="output-container">
                    <div className="output-text expandable">
                      {agent.output}
                    </div>
                    {agent.output.length > 200 && (
                      <button 
                        className="expand-btn"
                        onClick={(e) => {
                          const container = e.currentTarget.previousElementSibling as HTMLElement;
                          const isExpanded = container.classList.contains('expanded');
                          if (isExpanded) {
                            container.classList.remove('expanded');
                            e.currentTarget.textContent = 'Show More';
                          } else {
                            container.classList.add('expanded');
                            e.currentTarget.textContent = 'Show Less';
                          }
                        }}
                      >
                        Show More
                      </button>
                    )}
                  </div>
                </div>
              )}

              <div className="agent-footer">
                <div className="agent-confidence">
                  Live Confidence: {(agent.confidence * 100).toFixed(1)}%
                </div>
                {agent.cotGuidance && (
                  <div className="cot-status">
                    <span className="cot-label">Chain of Thought Guidance Applied</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AgentGrid;
