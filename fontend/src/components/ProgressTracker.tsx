import { ProgressStep, StageAssessment } from '../types';

interface ProgressTrackerProps {
  currentStep: number;
  status: string;
  processingTime: number;
  stageAssessments?: StageAssessment[];
}

const ProgressTracker = ({ currentStep, status, processingTime, stageAssessments = [] }: ProgressTrackerProps) => {
  const steps: ProgressStep[] = [
    { id: 1, name: 'Baseline', description: 'Generating baseline responses', status: 'pending' },
    { id: 2, name: 'Economic', description: 'Economic perspective analysis', status: 'pending' },
    { id: 3, name: 'Environmental', description: 'Environmental perspective analysis', status: 'pending' },
    { id: 4, name: 'Technological', description: 'Technological perspective analysis', status: 'pending' },
    { id: 5, name: 'Judge', description: 'Judge evaluation and synthesis', status: 'pending' },
    { id: 6, name: 'Complete', description: 'Analysis complete', status: 'pending' }
  ];

  const getStepStatus = (stepId: number) => {
    if (stepId < currentStep) return 'completed';
    if (stepId === currentStep) return 'active';
    return 'pending';
  };

  const getStageAssessment = (stepName: string) => {
    const stageName = stepName.toLowerCase();
    return stageAssessments.find(assessment => 
      assessment.stage.includes(stageName) || stageName.includes(assessment.stage)
    );
  };

  return (
    <div className="progress-tracker">
      <div className="progress-header">
        <h3>Analysis Progress</h3>
        <div className="progress-info">
          <span className="status-badge status-{status}">{status}</span>
          {processingTime > 0 && (
            <span className="processing-time">{processingTime.toFixed(1)}s</span>
          )}
        </div>
      </div>
      
      <div className="progress-steps">
        {steps.map((step, index) => {
          const stepStatus = getStepStatus(step.id);
          const assessment = getStageAssessment(step.name);
          
          return (
            <div key={step.id} className="progress-step-container">
              <div className={`progress-step ${stepStatus}`}>
                <div className="step-indicator">
                  {stepStatus === 'completed' ? '✓' : step.id}
                </div>
                <div className="step-content">
                  <div className="step-name">{step.name}</div>
                  <div className="step-description">{step.description}</div>
                  {assessment && (
                    <div className="step-assessment">
                      <div className="assessment-text">
                        Judge Assessment: {assessment.assessment.substring(0, 100)}
                        {assessment.assessment.length > 100 ? '...' : ''}
                      </div>
                      <div className="assessment-meta">
                        <span className="confidence">Confidence: {(assessment.confidence * 100).toFixed(0)}%</span>
                        <span className="timestamp">{assessment.timestamp}</span>
                      </div>
                    </div>
                  )}
                </div>
              </div>
              {index < steps.length - 1 && (
                <div className={`step-connector ${stepStatus === 'completed' ? 'completed' : ''}`} />
              )}
            </div>
          );
        })}
      </div>
      
      {/* Judge Assessments Summary */}
      {stageAssessments.length > 0 && (
        <div className="assessments-summary">
          <h4>Judge Assessments Overview</h4>
          <div className="assessments-grid">
            {stageAssessments.map((assessment, index) => (
              <div key={index} className="assessment-card">
                <div className="assessment-header">
                  <span className="stage-name">{assessment.stage}</span>
                  <span className="confidence-score">{(assessment.confidence * 100).toFixed(0)}%</span>
                </div>
                <div className="assessment-content">
                  {assessment.assessment}
                </div>
                <div className="assessment-timestamp">{assessment.timestamp}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ProgressTracker;
