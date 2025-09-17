import { useState, useEffect } from 'react';
import Header from './components/Header';
import QueryInput from './components/QueryInput';
import AgentGrid from './components/AgentGrid';
import ProgressTracker from './components/ProgressTracker';
import Results from './components/Results';
import LiveResponseFeed from './components/LiveResponseFeed';
import ErrorBoundary from './components/ErrorBoundary';
import { AnalysisState, AgentStatus, AgentResponse, StageAssessment, BaselineResponse, MultiPerspectiveAnalysis } from './types';
import { useWebSocket } from './hooks/useWebSocket';
import './App.css';

function App() {
  const [analysisState, setAnalysisState] = useState<AnalysisState>({
    query: '',
    status: 'idle',
    currentStep: 0,
    agents: {
      claude: { status: 'idle', perspective: 'baseline', output: '', confidence: 0 },
      gpt: { status: 'idle', perspective: 'baseline', output: '', confidence: 0 },
      grok: { status: 'idle', perspective: 'baseline', output: '', confidence: 0 },
      judge: { status: 'idle', perspective: 'synthesis', output: '', confidence: 0 }
    },
    results: null,
    processingTime: 0,
    liveResponses: [],
    stageAssessments: [],
    baselineResponses: {},
    multiPerspectiveAnalyses: {}
  });

  const { sendMessage, lastMessage, connectionStatus } = useWebSocket('ws://localhost:8001');

  useEffect(() => {
    if (lastMessage) {
      handleWebSocketMessage(lastMessage);
    }
  }, [lastMessage]);

  const handleWebSocketMessage = (message: any) => {
    try {
      const data = JSON.parse(message.data);
      
      switch (data.type) {
        case 'analysis_started':
          setAnalysisState(prev => ({
            ...prev,
            status: 'running',
            currentStep: 1,
            query: data.query,
            liveResponses: [],
            stageAssessments: [],
            baselineResponses: {},
            multiPerspectiveAnalyses: {}
          }));
          break;
          
        case 'judge_assessment':
          // Handle judge assessments at each stage
          const stageAssessment: StageAssessment = {
            stage: data.stage || 'initial',
            assessment: data.assessment || data.output || '',
            timestamp: new Date().toLocaleTimeString(),
            confidence: data.confidence || 0.9
          };

          setAnalysisState(prev => ({
            ...prev,
            stageAssessments: [...prev.stageAssessments, stageAssessment],
            agents: {
              ...prev.agents,
              judge: {
                ...prev.agents.judge,
                status: data.status as AgentStatus || 'completed',
                perspective: `judge_${data.stage}` as any,
                output: data.assessment || data.output || '',
                confidence: data.confidence || 0.9,
                step: data.step || prev.currentStep
              }
            }
          }));
          break;
          
        case 'baseline_response':
          // Handle baseline responses
          const baselineResponse: BaselineResponse = {
            content: data.content || data.output || '',
            confidence: data.confidence || 0.7,
            timestamp: new Date().toLocaleTimeString()
          };

          setAnalysisState(prev => ({
            ...prev,
            baselineResponses: {
              ...prev.baselineResponses,
              [data.agent]: baselineResponse
            }
          }));
          break;
          
        case 'agent_update':
          // Add to live responses feed
          const newResponse: AgentResponse = {
            id: `${data.agent}-${Date.now()}-${Math.random()}`,
            timestamp: new Date().toLocaleTimeString(),
            agent: data.agent,
            perspective: data.perspective || 'baseline',
            status: data.status,
            response: data.output || 'Processing...',
            confidence: data.confidence || 0,
            step: data.step || 1,
            cotApplied: data.cotGuidance,
            isJudgeAssessment: data.isJudgeAssessment || false
          };

          setAnalysisState(prev => ({
            ...prev,
            agents: {
              ...prev.agents,
              [data.agent]: {
                ...prev.agents[data.agent as keyof typeof prev.agents],
                status: data.status as AgentStatus,
                perspective: data.perspective || prev.agents[data.agent as keyof typeof prev.agents].perspective,
                output: data.output || prev.agents[data.agent as keyof typeof prev.agents].output,
                confidence: data.confidence || prev.agents[data.agent as keyof typeof prev.agents].confidence,
                cotGuidance: data.cotGuidance,
                step: data.step || prev.currentStep
              }
            },
            liveResponses: [newResponse, ...prev.liveResponses]
          }));
          break;
          
        case 'step_complete':
          setAnalysisState(prev => ({
            ...prev,
            currentStep: data.step
          }));
          break;
          
        case 'multi_perspective_update':
          // Handle multi-perspective analysis updates
          const perspectiveAnalysis: MultiPerspectiveAnalysis = {
            step1_economic: data.step1_economic,
            step2_economic_environmental: data.step2_economic_environmental,
            step3_complete_synthesis: data.step3_complete_synthesis,
            final_confidence: data.final_confidence,
            reasoning_evolution: data.reasoning_evolution || []
          };

          setAnalysisState(prev => ({
            ...prev,
            multiPerspectiveAnalyses: {
              ...prev.multiPerspectiveAnalyses,
              [data.agent]: perspectiveAnalysis
            }
          }));
          break;
          
        case 'analysis_complete':
          console.log('Enhanced analysis complete received:', data);
          console.log('Results:', data.results);
          console.log('Processing time:', data.processing_time);
          
          setAnalysisState(prev => ({
            ...prev,
            status: 'completed',
            results: data.results,
            processingTime: data.processing_time || 0,
            // Merge in any baseline responses and multi-perspective analyses from final results
            baselineResponses: {
              ...prev.baselineResponses,
              ...(data.results?.baseline_responses || {})
            },
            multiPerspectiveAnalyses: {
              ...prev.multiPerspectiveAnalyses,
              ...(data.results?.multi_perspective_analyses || {})
            }
          }));
          break;
          
        case 'error':
          setAnalysisState(prev => ({
            ...prev,
            status: 'error'
          }));
          console.error('Analysis error:', data.message);
          break;
      }
    } catch (error) {
      console.error('Error parsing WebSocket message:', error);
    }
  };

  const handleStartAnalysis = (queryData: {
    query: string;
    universalCot: string;
    perspectiveCots: { [key: string]: string };
  }) => {
    if (connectionStatus === 'Connected') {
      sendMessage({
        type: 'start_analysis',
        ...queryData
      });
      
      // Reset state for new analysis
      setAnalysisState(prev => ({
        ...prev,
        status: 'starting',
        currentStep: 0,
        agents: {
          claude: { status: 'idle', perspective: 'baseline', output: '', confidence: 0 },
          gpt: { status: 'idle', perspective: 'baseline', output: '', confidence: 0 },
          grok: { status: 'idle', perspective: 'baseline', output: '', confidence: 0 },
          judge: { status: 'idle', perspective: 'synthesis', output: '', confidence: 0 }
        },
        results: null,
        processingTime: 0,
        liveResponses: [],
        stageAssessments: [],
        baselineResponses: {},
        multiPerspectiveAnalyses: {}
      }));
    } else {
      console.error('WebSocket not connected');
    }
  };

  return (
    <div className="app">
      <Header connectionStatus={connectionStatus} />
      
      <main className="main-content">
        <div className="content-container">
          {/* Query Input Section */}
          <section className="query-section">
            <QueryInput 
              onStartAnalysis={handleStartAnalysis}
              disabled={analysisState.status === 'running' || analysisState.status === 'starting'}
            />
          </section>

          {/* Progress Tracker with Judge Assessments */}
          {analysisState.status !== 'idle' && (
            <section className="progress-section">
              <ProgressTracker 
                currentStep={analysisState.currentStep}
                status={analysisState.status}
                processingTime={analysisState.processingTime}
                stageAssessments={analysisState.stageAssessments}
              />
            </section>
          )}

          {/* Real-time Agent Grid with Enhanced Display */}
          {analysisState.status !== 'idle' && (
            <section className="agents-section">
              <AgentGrid 
                agents={analysisState.agents}
                currentStep={analysisState.currentStep}
                baselineResponses={analysisState.baselineResponses}
                multiPerspectiveAnalyses={analysisState.multiPerspectiveAnalyses}
              />
            </section>
          )}

          {/* Enhanced Live Response Feed */}
          {analysisState.status !== 'idle' && (
            <section className="live-feed-section">
              <LiveResponseFeed 
                responses={analysisState.liveResponses}
                stageAssessments={analysisState.stageAssessments}
                showCoTGuidance={true}
                showJudgeAssessments={true}
              />
            </section>
          )}

          {/* Enhanced Final Results */}
          {analysisState.results && (
            <section className="results-section">
              <ErrorBoundary>
                <Results 
                  results={analysisState.results}
                  processingTime={analysisState.processingTime || 0}
                  baselineResponses={analysisState.baselineResponses}
                  multiPerspectiveAnalyses={analysisState.multiPerspectiveAnalyses}
                  stageAssessments={analysisState.stageAssessments}
                />
              </ErrorBoundary>
            </section>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
