from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from enum import Enum

class Perspective(str, Enum):
    """Available analytical perspectives"""
    ECONOMIC = "economic"
    ENVIRONMENTAL = "environmental"
    TECHNOLOGICAL = "technological"

class ModelType(str, Enum):
    """Enumeration of available model types"""
    CLAUDE = "claude"
    GPT = "gpt"
    GROK = "grok"
    JUDGE = "judge"

class PerspectiveResponse(BaseModel):
    """Response from a model for a specific perspective"""
    perspective: Perspective
    content: str
    reasoning: str = ""
    confidence: float = 0.0
    metadata: Dict[str, Any] = {}
    
    class Config:
        protected_namespaces = ()

class BaselineResponse(BaseModel):
    """Raw baseline response without any guidance"""
    model_type: ModelType
    content: str
    confidence: float = 0.0
    metadata: Dict[str, Any] = {}
    
    class Config:
        protected_namespaces = ()

class MultiPerspectiveAnalysis(BaseModel):
    """Complete multi-perspective analysis from one model"""
    model_type: ModelType
    baseline_response: BaselineResponse = None
    step1_economic: PerspectiveResponse = None
    step2_economic_environmental: str = ""
    step3_complete_synthesis: str = ""
    final_confidence: float = 0.0
    reasoning_evolution: List[str] = []
    
    class Config:
        protected_namespaces = ()

class InputPackage(BaseModel):
    """Validated input package for multi-perspective analysis"""
    query: str
    perspective_1: str = "economic"
    perspective_2: str = "environmental" 
    perspective_3: str = "technological"
    universal_cot: str = ""
    perspective_specific_cots: Dict[str, str] = {}
    
    def validate_inputs(self) -> bool:
        """Validate that all required inputs are provided"""
        if not self.query.strip():
            raise ValueError("Query is required")
        return True

class MultiPerspectiveEnsembleState(BaseModel):
    """Enhanced state for multi-perspective ensemble analysis"""
    
    # Input Package
    input_package: InputPackage
    
    # Baseline Responses (raw, no guidance)
    claude_baseline: BaselineResponse = None
    gpt_baseline: BaselineResponse = None
    grok_baseline: BaselineResponse = None
    
    # Multi-Perspective Analyses
    claude_analysis: MultiPerspectiveAnalysis = None
    gpt_analysis: MultiPerspectiveAnalysis = None
    grok_analysis: MultiPerspectiveAnalysis = None
    
    # Judge Assessments at Each Stage
    judge_initial_assessment: str = ""
    judge_step1_assessment: str = ""
    judge_step2_assessment: str = ""
    judge_step3_assessment: str = ""
    
    # Final Judge Analysis
    judge_analysis: str = ""
    agreements_disagreements: str = ""
    best_insights: str = ""
    final_synthesis: str = ""
    methodology_assessment: str = ""
    quality_scores: Dict[str, float] = {}
    
    # Performance Comparison
    baseline_comparison: Dict[str, Any] = {}
    improvement_metrics: Dict[str, float] = {}
    quality_analysis: Dict[str, Any] = {}
    methodology_effectiveness: Dict[str, Any] = {}
    
    # Control flags
    baselines_complete: bool = False
    step1_complete: bool = False
    step2_complete: bool = False
    step3_complete: bool = False
    judging_complete: bool = False
    logging_complete: bool = False
    
    # Metadata
    processing_time: float = 0.0
    total_tokens_used: int = 0
    
    class Config:
        arbitrary_types_allowed = True
