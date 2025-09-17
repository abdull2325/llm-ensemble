import React from 'react';
import { AgentResponse, StageAssessment } from '../types';
import './LiveResponseFeed.css';

interface LiveResponseFeedProps {
  responses: AgentResponse[];
  stageAssessments?: StageAssessment[];
  showCoTGuidance?: boolean;
  showJudgeAssessments?: boolean;
}

const LiveResponseFeed: React.FC<LiveResponseFeedProps> = ({ 
  responses, 
  stageAssessments = [], 
  showCoTGuidance = true,
  showJudgeAssessments = true 
}) => {
  const getAgentColor = (agent: string) => {
    const colors = {
      claude: '#ff9999', // Light coral
      gpt: '#99ccff',    // Light blue
      grok: '#99ff99',   // Light green
      judge: '#ffcc99'   // Light orange
    };
    return colors[agent as keyof typeof colors] || '#e0e0e0';
  };

  const getStepName = (step: number) => {
    const steps = {
      1: 'Baseline Analysis',
      2: 'Economic Perspective',
      3: 'Environmental Perspective', 
      4: 'Technological Synthesis',
      5: 'Judge Evaluation',
      6: 'Complete'
    };
    return steps[step as keyof typeof steps] || `Step ${step}`;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'thinking': return '🤔';
      case 'completed': return '✅';
      case 'idle': return '⏸️';
      default: return '⚡';
    }
  };

  // Combine responses and stage assessments for chronological display
  const getAllEvents = () => {
    const events: Array<{
      type: 'response' | 'assessment';
      data: AgentResponse | StageAssessment;
      timestamp: string;
      sortKey: number;
    }> = [];
    
    // Add responses
    responses.forEach(response => {
      events.push({
        type: 'response',
        data: response,
        timestamp: response.timestamp,
        sortKey: new Date(`1970-01-01 ${response.timestamp}`).getTime()
      });
    });
    
    // Add stage assessments if showing them
    if (showJudgeAssessments) {
      stageAssessments.forEach(assessment => {
        events.push({
          type: 'assessment',
          data: assessment,
          timestamp: assessment.timestamp,
          sortKey: new Date(`1970-01-01 ${assessment.timestamp}`).getTime()
        });
      });
    }
    
    // Sort by timestamp (most recent first)
    return events.sort((a, b) => b.sortKey - a.sortKey);
  };

  const allEvents = getAllEvents();

  return (
    <div className="live-response-feed">
      <div className="feed-header">
        <h3>🔴 Live Agent Response Feed</h3>
        <div className="feed-controls">
          <span className="response-count">{responses.length} responses</span>
          {showJudgeAssessments && stageAssessments.length > 0 && (
            <span className="assessment-count">{stageAssessments.length} assessments</span>
          )}
        </div>
      </div>
      
      <div className="feed-container">
        {allEvents.length === 0 ? (
          <div className="empty-feed">
            <p>No responses yet. Start an analysis to see live agent responses.</p>
          </div>
        ) : (
          <div className="responses-list">
            {allEvents.map((event, index) => {
              if (event.type === 'response') {
                const response = event.data as AgentResponse;
                return (
                  <div 
                    key={response.id} 
                    className={`response-item ${response.isJudgeAssessment ? 'judge-assessment' : 'agent-response'}`}
                    style={{ borderLeftColor: getAgentColor(response.agent) }}
                  >
                    <div className="response-header">
                      <div className="response-meta">
                        <span className="agent-badge" style={{ backgroundColor: getAgentColor(response.agent) }}>
                          {response.agent.toUpperCase()}
                        </span>
                        <span className="step-badge">
                          {getStepName(response.step)}
                        </span>
                        <span className="perspective-badge">
                          {response.perspective}
                        </span>
                        <span className="status-indicator">
                          {getStatusIcon(response.status)} {response.status}
                        </span>
                        {response.isJudgeAssessment && (
                          <span className="judge-indicator">Judge Assessment</span>
                        )}
                        {showCoTGuidance && response.cotApplied && (
                          <span className="cot-indicator">CoT Applied</span>
                        )}
                      </div>
                      <div className="response-timestamp">
                        {response.timestamp}
                      </div>
                    </div>
                    
                    <div className="response-content">
                      <div className="response-text">
                        {response.response}
                      </div>
                      
                      <div className="response-footer">
                        <div className="confidence-meter">
                          <span className="confidence-label">Confidence:</span>
                          <div className="confidence-bar">
                            <div 
                              className="confidence-fill"
                              style={{ width: `${response.confidence * 100}%` }}
                            ></div>
                          </div>
                          <span className="confidence-value">
                            {Math.round(response.confidence * 100)}%
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              } else {
                // Stage Assessment
                const assessment = event.data as StageAssessment;
                return (
                  <div 
                    key={`assessment-${index}`}
                    className="response-item stage-assessment"
                    style={{ borderLeftColor: '#96ceb4' }}
                  >
                    <div className="response-header">
                      <div className="response-meta">
                        <span className="agent-badge judge-badge">
                          JUDGE
                        </span>
                        <span className="stage-badge">
                          {assessment.stage.toUpperCase()} ASSESSMENT
                        </span>
                        <span className="status-indicator">
                          ⚖️ assessment
                        </span>
                      </div>
                      <div className="response-timestamp">
                        {assessment.timestamp}
                      </div>
                    </div>
                    
                    <div className="response-content">
                      <div className="response-text assessment-text">
                        {assessment.assessment}
                      </div>
                      
                      <div className="response-footer">
                        <div className="confidence-meter">
                          <span className="confidence-label">Judge Confidence:</span>
                          <div className="confidence-bar judge-confidence">
                            <div 
                              className="confidence-fill"
                              style={{ width: `${assessment.confidence * 100}%` }}
                            ></div>
                          </div>
                          <span className="confidence-value">
                            {Math.round(assessment.confidence * 100)}%
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              }
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default LiveResponseFeed;
