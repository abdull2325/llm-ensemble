import { AnalysisResults, BaselineResponse, MultiPerspectiveAnalysis, StageAssessment } from '../types';

interface ResultsProps {
  results: AnalysisResults;
  processingTime: number;
  baselineResponses?: Record<string, BaselineResponse>;
  multiPerspectiveAnalyses?: Record<string, MultiPerspectiveAnalysis>;
  stageAssessments?: StageAssessment[];
}

const Results = ({ 
  results, 
  processingTime, 
  baselineResponses = {}, 
  multiPerspectiveAnalyses = {},
  stageAssessments = []
}: ResultsProps) => {
  // Add error handling for potential issues
  if (!results) {
    return (
      <div className="results-container">
        <div className="error-message">No results available</div>
      </div>
    );
  }

  // Debug logging
  console.log('Results props received:');
  console.log('Baseline responses:', baselineResponses);
  console.log('Multi-perspective analyses:', multiPerspectiveAnalyses);
  console.log('Stage assessments:', stageAssessments);
  console.log('Baseline responses keys:', Object.keys(baselineResponses));
  console.log('Multi-perspective analyses keys:', Object.keys(multiPerspectiveAnalyses));
  console.log('Stage assessments length:', stageAssessments.length);  const safeProcessingTime = typeof processingTime === 'number' ? processingTime : 0;

  // Helper function to format text content with proper structure
  const formatTextContent = (text: string) => {
    if (!text) return null;
    
    // Split by major sections and format them
    const sections = text.split(/(?=\b(?:Economic|Environmental|Technological|METHODOLOGY_ASSESSMENT)\b)/);
    
    return (
      <div className="formatted-content">
        {sections.map((section, index) => {
          if (!section.trim()) return null;
          
          // Check if this is a major section header
          const isMajorSection = /^(Economic|Environmental|Technological|METHODOLOGY_ASSESSMENT)/.test(section.trim());
          
          if (isMajorSection) {
            const [header, ...contentParts] = section.split(':');
            const content = contentParts.join(':').trim();
            
            return (
              <div key={index} className="content-section">
                <h6 className="section-header">{header.trim()}:</h6>
                <div className="section-content">
                  {formatBulletPoints(content)}
                </div>
              </div>
            );
          } else {
            // Regular paragraph content
            return (
              <div key={index} className="content-paragraph">
                {formatBulletPoints(section)}
              </div>
            );
          }
        })}
      </div>
    );
  };

  // Helper function to format bullet points and lists
  const formatBulletPoints = (text: string) => {
    if (!text) return null;
    
    // Split by lines and process each one
    const lines = text.split('\n').filter(line => line.trim());
    
    return (
      <div className="formatted-text">
        {lines.map((line, index) => {
          const trimmedLine = line.trim();
          if (!trimmedLine) return null;
          
          // Check for numbered lists (1., 2., etc.)
          const numberedMatch = trimmedLine.match(/^(\d+\.)\s*(.*)$/);
          if (numberedMatch) {
            return (
              <div key={index} className="numbered-point">
                <span className="number">{numberedMatch[1]}</span>
                <span className="numbered-content">{numberedMatch[2]}</span>
              </div>
            );
          }
          
          // Check for bullet points (-, •, or standalone •)
          if (trimmedLine.startsWith('-') || trimmedLine.startsWith('•') || trimmedLine === '•') {
            const content = trimmedLine.replace(/^[-•]\s*/, '').trim();
            if (!content) {
              // Standalone bullet, likely followed by content on next lines
              return (
                <div key={index} className="bullet-point">
                  <span className="bullet">•</span>
                  <span className="bullet-content">
                    {/* Look ahead for content */}
                    {lines[index + 1] && !lines[index + 1].startsWith('-') && !lines[index + 1].startsWith('•') 
                      ? lines[index + 1].trim() 
                      : ''}
                  </span>
                </div>
              );
            }
            return (
              <div key={index} className="bullet-point">
                <span className="bullet">•</span>
                <span className="bullet-content">{content}</span>
              </div>
            );
          }
          
          // Check for bold headers (### or **)
          if (trimmedLine.startsWith('###') || (trimmedLine.startsWith('**') && trimmedLine.endsWith('**'))) {
            const headerText = trimmedLine.replace(/^###\s*/, '').replace(/^\*\*/, '').replace(/\*\*$/, '');
            return (
              <h6 key={index} className="formatted-header">
                {headerText}
              </h6>
            );
          }
          
          // Skip lines that are just continuation of previous bullet points
          if (index > 0 && lines[index - 1] === '•' && !trimmedLine.startsWith('-') && !trimmedLine.startsWith('•')) {
            return null; // Already handled in the bullet point above
          }
          
          // Regular text paragraph
          return (
            <p key={index} className="text-paragraph">
              {trimmedLine}
            </p>
          );
        })}
      </div>
    );
  };

  // Helper function to format metric names for better readability
  const formatMetricName = (key: string): string => {
    const formatMap: { [key: string]: string } = {
      'claude_length_improvement': 'Claude Analysis Length Improvement',
      'gpt_length_improvement': 'GPT Analysis Length Improvement', 
      'grok_length_improvement': 'Grok Analysis Length Improvement',
      'confidence_improvement': 'Confidence Improvement',
      'average_final_confidence': 'Average Final Confidence',
      'average_baseline_confidence': 'Average Baseline Confidence',
      'average_length_improvement': 'Average Length Improvement',
      'comprehensiveness_improvement': 'Comprehensiveness Improvement',
      'claude_baseline_vs_ensemble': 'Claude: Baseline vs Ensemble',
      'gpt_baseline_vs_ensemble': 'GPT: Baseline vs Ensemble',
      'grok_baseline_vs_ensemble': 'Grok: Baseline vs Ensemble',
      'baseline_length': 'Baseline Length',
      'ensemble_length': 'Ensemble Length',
      'length_ratio': 'Length Ratio'
    };
    
    return formatMap[key] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  // Helper function to format metric values with appropriate units
  const formatMetricValue = (value: any, key?: string): string => {
    if (typeof value === 'boolean') return value ? 'Yes' : 'No';
    if (typeof value === 'number') {
      // Handle percentages
      if (key && (key.includes('confidence') || key.includes('ratio'))) {
        if (value <= 1) {
          return `${(value * 100).toFixed(1)}%`;
        }
        return `${value.toFixed(2)}x`;
      }
      // Handle length measurements
      if (key && key.includes('length')) {
        return `${value.toLocaleString()} chars`;
      }
      return value.toFixed(2);
    }
    if (Array.isArray(value)) return value.join(', ');
    return String(value);
  };

  // Enhanced helper function to render nested object data with better formatting
  const renderObjectSection = (obj: any, title: string) => {
    if (!obj || typeof obj !== 'object' || Object.keys(obj).length === 0) return null;

    return (
      <div className="comparison-section">
        <h5>{title}</h5>
        <div className="comparison-grid">
          {Object.entries(obj).map(([key, value]) => (
            <div key={key} className="comparison-item">
              <span className="metric-label">{formatMetricName(key)}:</span>
              <span className="metric-value">{formatMetricValue(value, key)}</span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="results-container">
      <h3>Enhanced Multi-Perspective Analysis Results</h3>
      <div className="processing-time">
        Completed in {safeProcessingTime.toFixed(2)} seconds
      </div>
      
      {/* Enhanced Judge Evaluation Section */}
      <div className="enhanced-judge-analysis">
        <h4>Judge Comprehensive Evaluation</h4>
        {results.judge_evaluation ? (
          <div className="judge-evaluation-enhanced">
            <div className="judge-synthesis">
              <h5>Final Synthesis</h5>
              <div className="synthesis-content">
                {formatTextContent(results.judge_evaluation.final_synthesis || "Comprehensive synthesis completed.")}
              </div>
            </div>
            
            {results.judge_evaluation.comparative_analysis && (
              <div className="comparative-analysis">
                <h5>Comparative Analysis</h5>
                <div className="comparison-content">
                  {formatTextContent(results.judge_evaluation.comparative_analysis)}
                </div>
              </div>
            )}
            
            {results.judge_evaluation.reasoning && (
              <div className="judge-reasoning">
                <h5>Judge Reasoning</h5>
                <div className="reasoning-content">
                  {formatTextContent(results.judge_evaluation.reasoning)}
                </div>
              </div>
            )}
            
            <div className="judge-confidence">
              <span>Judge Final Confidence: </span>
              <span className="confidence-score">
                {((results.judge_evaluation.confidence || 0) * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        ) : (
          <div className="judge-content">
            {results.judge_analysis || "Judge evaluation completed successfully."}
          </div>
        )}
      </div>

      {/* Stage Assessments Timeline */}
      {stageAssessments.length > 0 && (
        <div className="stage-assessments-timeline">
          <h4>Judge Assessments Timeline</h4>
          <div className="assessments-list">
            {stageAssessments.map((assessment, index) => (
              <div key={index} className="assessment-item">
                <div className="assessment-header">
                  <span className="stage-name">{assessment.stage.toUpperCase()}</span>
                  <span className="assessment-time">{assessment.timestamp}</span>
                  <span className="assessment-confidence">
                    {(assessment.confidence * 100).toFixed(0)}% confidence
                  </span>
                </div>
                <div className="assessment-content">
                  {assessment.assessment}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Baseline vs Enhanced Comparison */}
      {Object.keys(baselineResponses).length > 0 && (
        <div className="baseline-enhanced-comparison">
          <h4>Baseline vs Enhanced Analysis Comparison</h4>
          {Object.entries(baselineResponses).map(([agent, baseline]) => (
            <div key={agent} className="agent-comparison">
              <h5>{agent.toUpperCase()} Agent Analysis Evolution</h5>
              
              {/* Baseline Response */}
              <div className="comparison-section baseline-section">
                <h6>Baseline Response</h6>
                <div className="response-content expandable-content">
                  <div className="content-wrapper">
                    {formatTextContent(baseline.content)}
                  </div>
                  {baseline.content.length > 1000 && (
                    <button 
                      className="expand-btn"
                      onClick={(e) => {
                        const wrapper = e.currentTarget.previousElementSibling as HTMLElement;
                        const isExpanded = wrapper.classList.contains('expanded');
                        if (isExpanded) {
                          wrapper.classList.remove('expanded');
                          e.currentTarget.textContent = 'Show More';
                        } else {
                          wrapper.classList.add('expanded');
                          e.currentTarget.textContent = 'Show Less';
                        }
                      }}
                    >
                      Show More
                    </button>
                  )}
                </div>
                <div className="response-meta">
                  <span>Confidence: {(baseline.confidence * 100).toFixed(0)}%</span>
                  <span>Time: {baseline.timestamp}</span>
                </div>
              </div>
              
              {/* Multi-Perspective Analysis */}
              {multiPerspectiveAnalyses[agent] && (
                <div className="comparison-section enhanced-section">
                  <h6>Enhanced Multi-Perspective Analysis</h6>
                  <div className="perspective-evolution">
                    {multiPerspectiveAnalyses[agent].step1_economic && (
                      <div className="perspective-step">
                        <strong>Economic Perspective:</strong>
                        <div className="step-content">
                          {formatTextContent(multiPerspectiveAnalyses[agent].step1_economic)}
                        </div>
                      </div>
                    )}
                    {multiPerspectiveAnalyses[agent].step2_economic_environmental && (
                      <div className="perspective-step">
                        <strong>Economic + Environmental:</strong>
                        <div className="step-content">
                          {formatTextContent(multiPerspectiveAnalyses[agent].step2_economic_environmental)}
                        </div>
                      </div>
                    )}
                    {multiPerspectiveAnalyses[agent].step3_complete_synthesis && (
                      <div className="perspective-step">
                        <strong>Complete Synthesis:</strong>
                        <div className="step-content">
                          {formatTextContent(multiPerspectiveAnalyses[agent].step3_complete_synthesis)}
                        </div>
                      </div>
                    )}
                  </div>
                  <div className="enhanced-meta">
                    <span>Final Confidence: {((multiPerspectiveAnalyses[agent].final_confidence || 0) * 100).toFixed(0)}%</span>
                    <span>Reasoning Steps: {multiPerspectiveAnalyses[agent].reasoning_evolution?.length || 0}</span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
      
      <div className="final-synthesis">
        <h4>Final Synthesis</h4>
        <div className="synthesis-content">
          {results.final_response || results.final_synthesis || "Enhanced multi-perspective analysis complete - see detailed comparisons above."}
        </div>
      </div>
      
      {/* Individual Agent Responses */}
      {results.agent_responses && (
        <div className="agent-responses">
          <h4>Individual Agent Responses</h4>
          {Object.entries(results.agent_responses).map(([agentName, responses]) => (
            <div key={agentName} className="agent-response-section">
              <h5>{agentName.charAt(0).toUpperCase() + agentName.slice(1)} Agent</h5>
              {Array.isArray(responses) ? responses.map((response, index) => (
                <div key={index} className="response-item">
                  <div className="response-perspective">{response?.perspective || 'Analysis'}</div>
                  <div className="response-content">{response?.output || response?.content || 'No content'}</div>
                  <div className="response-confidence">Confidence: {((response?.confidence || 0) * 100).toFixed(1)}%</div>
                </div>
              )) : (
                <div className="response-item">
                  <div className="response-content">{responses?.output || responses?.content || String(responses) || 'No content'}</div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
      
      <div className="quality-scores">
        <h4>Enhanced Quality Scores</h4>
        <div className="scores-grid">
          {results.consensus_confidence && (
            <div className="score-item">
              <span>Consensus Confidence:</span>
              <span>{(results.consensus_confidence * 100).toFixed(1)}%</span>
            </div>
          )}
          {results.total_tokens && (
            <div className="score-item">
              <span>Total Tokens:</span>
              <span>{Math.round(results.total_tokens)}</span>
            </div>
          )}
          {results.agents_consulted && (
            <div className="score-item">
              <span>Agents Consulted:</span>
              <span>{results.agents_consulted}</span>
            </div>
          )}
          {stageAssessments.length > 0 && (
            <div className="score-item">
              <span>Judge Assessments:</span>
              <span>{stageAssessments.length} stages</span>
            </div>
          )}
          {Object.keys(baselineResponses).length > 0 && (
            <div className="score-item">
              <span>Baseline Comparisons:</span>
              <span>{Object.keys(baselineResponses).length} agents</span>
            </div>
          )}
          {results.quality_scores && Object.entries(results.quality_scores).map(([key, score]) => (
            <div key={key} className="score-item">
              <span>{key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</span>
              <span>{(Number(score) * 100).toFixed(1)}%</span>
            </div>
          ))}
        </div>
      </div>
      
      {/* Enhanced Performance Comparison */}
      {results.performance_comparison && (
        <div className="performance-comparison">
          <h4>Enhanced Performance Comparison</h4>
          
          {renderObjectSection(results.performance_comparison.baseline_comparison, "Baseline vs Enhanced Comparison")}
          {renderObjectSection(results.performance_comparison.improvement_metrics, "Improvement Metrics")}
          {renderObjectSection(results.performance_comparison.multi_perspective_advantage, "Multi-Perspective Advantage")}
          
          {/* Enhancement Summary */}
          <div className="enhancement-summary">
            <h5>Enhancement Summary</h5>
            <div className="enhancement-stats">
              <div className="stat-item">
                <span>CoT Integration:</span>
                <span>✅ Applied across all perspectives</span>
              </div>
              <div className="stat-item">
                <span>Judge Oversight:</span>
                <span>✅ {stageAssessments?.length || 0} stage assessment{(stageAssessments?.length || 0) !== 1 ? 's' : ''}</span>
              </div>
              <div className="stat-item">
                <span>Baseline Comparison:</span>
                <span>✅ {Object.keys(baselineResponses || {}).length} agent comparison{Object.keys(baselineResponses || {}).length !== 1 ? 's' : ''}</span>
              </div>
              <div className="stat-item">
                <span>Multi-Perspective Evolution:</span>
                <span>✅ {Object.keys(multiPerspectiveAnalyses || {}).length} agent progression{Object.keys(multiPerspectiveAnalyses || {}).length !== 1 ? 's' : ''}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Results;
