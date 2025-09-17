export type AgentStatus = 'idle' | 'thinking' | 'processing' | 'completed' | 'error';

export type Perspective = 'baseline' | 'economic' | 'environmental' | 'technological' | 'synthesis' | 'judge_initial' | 'judge_step1' | 'judge_step2' | 'judge_step3';

export type AnalysisStatus = 'idle' | 'starting' | 'running' | 'completed' | 'error';

export interface AgentState {
  status: AgentStatus;
  perspective: Perspective;
  output: string;
  confidence: number;
  reasoning?: string;
  metadata?: Record<string, any>;
  cotGuidance?: string;
  step?: number;
}

export interface AnalysisState {
  query: string;
  status: AnalysisStatus;
  currentStep: number;
  agents: {
    claude: AgentState;
    gpt: AgentState;
    grok: AgentState;
    judge: AgentState;
  };
  results: AnalysisResults | null;
  processingTime: number;
  liveResponses: AgentResponse[];
  stageAssessments: StageAssessment[];
  baselineResponses: Record<string, BaselineResponse>;
  multiPerspectiveAnalyses: Record<string, MultiPerspectiveAnalysis>;
}

export interface AgentResponse {
  id: string;
  timestamp: string;
  agent: string;
  perspective: string;
  status: string;
  response: string;
  confidence: number;
  step: number;
  cotApplied?: string;
  isJudgeAssessment?: boolean;
}

export interface BaselineResponse {
  content: string;
  confidence: number;
  timestamp: string;
}

export interface MultiPerspectiveAnalysis {
  step1_economic?: string;
  step2_economic_environmental?: string;
  step3_complete_synthesis?: string;
  final_confidence?: number;
  reasoning_evolution?: string[];
}

export interface StageAssessment {
  stage: 'initial' | 'step1' | 'step2' | 'step3' | 'final';
  assessment: string;
  timestamp: string;
  confidence: number;
}

export interface AnalysisResults {
  final_synthesis?: string;
  final_response?: string;
  judge_analysis?: string;
  judge_evaluation?: {
    initial_assessment?: string;
    step1_assessment?: string;
    step2_assessment?: string;
    step3_assessment?: string;
    final_evaluation?: string;
    final_synthesis?: string;
    methodology_assessment?: string;
    agreements_disagreements?: string;
    best_insights?: string;
    quality_scores?: Record<string, number>;
    [key: string]: any;
  };
  baseline_responses?: Record<string, BaselineResponse>;
  multi_perspective_analyses?: Record<string, MultiPerspectiveAnalysis>;
  performance_comparison?: {
    baseline_comparison?: Record<string, any>;
    improvement_metrics?: Record<string, number>;
    quality_analysis?: Record<string, any>;
    methodology_effectiveness?: Record<string, any>;
    [key: string]: any;
  };
  quality_scores?: Record<string, number>;
  baseline_comparison?: Record<string, any>;
  improvement_metrics?: Record<string, number>;
  completion_status?: Record<string, boolean>;
  consensus_confidence?: number;
  total_tokens?: number;
  agents_consulted?: number;
  agent_responses?: Record<string, any>;
  [key: string]: any;
}

export interface QueryInputData {
  query: string;
  universalCot: string;
  perspectiveCots: {
    economic: string;
    environmental: string;
    technological: string;
  };
}

export interface WebSocketMessage {
  type: string;
  data?: any;
  agent?: string;
  status?: AgentStatus;
  perspective?: Perspective;
  output?: string;
  confidence?: number;
  step?: number;
  query?: string;
  results?: AnalysisResults;
  processing_time?: number;
  message?: string;
  cotGuidance?: string;
  isJudgeAssessment?: boolean;
  stage?: string;
  assessment?: string;
}

export type ConnectionStatus = 'Connecting' | 'Connected' | 'Disconnected' | 'Error';

export interface ProgressStep {
  id: number;
  name: string;
  description: string;
  status: 'pending' | 'active' | 'completed' | 'error';
  judgeAssessment?: string;
}

export interface AgentConfig {
  name: string;
  displayName: string;
  color: string;
  accentColor: string;
  icon: string;
  description: string;
}
