from typing import Dict, Any
import asyncio
from graph.multi_perspective_state import (
    MultiPerspectiveEnsembleState, 
    MultiPerspectiveAnalysis,
    PerspectiveResponse,
    BaselineResponse,
    ModelType,
    Perspective
)
from models.claude_model import ClaudeModel
from models.gpt_model import GPTModel
from models.grok_model import GrokModel
from utils.memory import MemoryLogger
from utils.judge import UnbiasedJudge
from utils.chain_of_thought import ChainOfThoughtEnhancer

class MultiPerspectiveNodes:
    """Node implementations for multi-perspective LangGraph ensemble workflow"""
    
    def __init__(self):
        self.claude_model = ClaudeModel()
        self.gpt_model = GPTModel()
        self.grok_model = GrokModel()
        self.memory_logger = MemoryLogger()
        self.judge = UnbiasedJudge()
        self.cot_enhancer = ChainOfThoughtEnhancer()
    
    async def baseline_analysis_node(self, state: MultiPerspectiveEnsembleState) -> Dict[str, Any]:
        """Generate raw baseline responses without any guidance + Judge initial assessment"""
        print("Generating baseline responses (no guidance)...")
        
        query = state.input_package.query
        
        # Simple prompt without any CoT or perspective guidance
        baseline_prompt = f"Please provide a comprehensive answer to this query: {query}"
        
        # Run all models in parallel for baseline
        tasks = [
            self._get_baseline_claude(baseline_prompt),
            self._get_baseline_gpt(baseline_prompt),
            self._get_baseline_grok(baseline_prompt)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        claude_baseline, gpt_baseline, grok_baseline = results
        
        updates = {"baselines_complete": True}
        
        if not isinstance(claude_baseline, Exception):
            updates["claude_baseline"] = claude_baseline
        if not isinstance(gpt_baseline, Exception):
            updates["gpt_baseline"] = gpt_baseline
        if not isinstance(grok_baseline, Exception):
            updates["grok_baseline"] = grok_baseline
        
        # Send query to judge for initial assessment
        print("Judge: Initial query assessment...")
        judge_initial_prompt = f"""
        You are evaluating a query that will be analyzed through a multi-perspective approach.
        
        QUERY: {query}
        
        Provide your initial assessment:
        INITIAL_ASSESSMENT: [Your direct analysis of this query]
        KEY_CONSIDERATIONS: [Important aspects to consider for multi-perspective analysis]
        EXPECTED_PERSPECTIVES: [How economic, environmental, and technological perspectives might differ]
        """
        
        try:
            judge_initial = await self.judge.judge_client.ainvoke(judge_initial_prompt)
            updates["judge_initial_assessment"] = judge_initial.content
        except Exception as e:
            updates["judge_initial_assessment"] = f"Error in initial judge assessment: {str(e)}"
            
        return updates
    
    async def step1_economic_analysis_node(self, state: MultiPerspectiveEnsembleState) -> Dict[str, Any]:
        """Step 1: Single perspective analysis (Economic) + Judge assessment"""
        print("💰 Step 1: Economic perspective analysis...")
        
        package = state.input_package
        economic_cot = package.perspective_specific_cots.get("economic", "")
        
        # Create economic perspective prompt
        economic_prompt = self._create_perspective_prompt(
            package.query,
            "economic",
            package.universal_cot,
            economic_cot
        )
        
        # Run all models for economic analysis
        tasks = [
            self._analyze_perspective_claude(economic_prompt, Perspective.ECONOMIC),
            self._analyze_perspective_gpt(economic_prompt, Perspective.ECONOMIC),
            self._analyze_perspective_grok(economic_prompt, Perspective.ECONOMIC)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        updates = {"step1_complete": True}
        
        # Process results and create MultiPerspectiveAnalysis objects
        if not isinstance(results[0], Exception):
            claude_analysis = MultiPerspectiveAnalysis(
                model_type=ModelType.CLAUDE,
                step1_economic=results[0],
                reasoning_evolution=["Step 1: Economic analysis completed"]
            )
            updates["claude_analysis"] = claude_analysis
            
        if not isinstance(results[1], Exception):
            gpt_analysis = MultiPerspectiveAnalysis(
                model_type=ModelType.GPT,
                step1_economic=results[1],
                reasoning_evolution=["Step 1: Economic analysis completed"]
            )
            updates["gpt_analysis"] = gpt_analysis
            
        if not isinstance(results[2], Exception):
            grok_analysis = MultiPerspectiveAnalysis(
                model_type=ModelType.GROK,
                step1_economic=results[2],
                reasoning_evolution=["Step 1: Economic analysis completed"]
            )
            updates["grok_analysis"] = grok_analysis
        
        # Judge assessment of Step 1 results
        print("Judge: Step 1 assessment...")
        step1_judge_prompt = f"""
        You are evaluating Step 1 of a multi-perspective analysis focused on the ECONOMIC perspective.
        
        ORIGINAL QUERY: {package.query}
        
        STEP 1 ECONOMIC ANALYSES:
        Claude: {results[0].content if not isinstance(results[0], Exception) else "Error"}
        GPT: {results[1].content if not isinstance(results[1], Exception) else "Error"}
        Grok: {results[2].content if not isinstance(results[2], Exception) else "Error"}
        
        BASELINE RESPONSES:
        Claude Baseline: {state.claude_baseline.content if state.claude_baseline else "N/A"}
        GPT Baseline: {state.gpt_baseline.content if state.gpt_baseline else "N/A"}
        Grok Baseline: {state.grok_baseline.content if state.grok_baseline else "N/A"}
        
        Assess:
        STEP1_ANALYSIS: [How well did each model analyze the economic perspective?]
        IMPROVEMENTS_OVER_BASELINE: [How do the economic analyses compare to baselines?]
        MISSING_ECONOMIC_ASPECTS: [What economic factors might be missing?]
        PREPARATION_FOR_STEP2: [How well positioned are these analyses for environmental integration?]
        """
        
        try:
            judge_step1 = await self.judge.judge_client.ainvoke(step1_judge_prompt)
            updates["judge_step1_assessment"] = judge_step1.content
        except Exception as e:
            updates["judge_step1_assessment"] = f"Error in Step 1 judge assessment: {str(e)}"
        
        return updates
    
    async def step2_environmental_analysis_node(self, state: MultiPerspectiveEnsembleState) -> Dict[str, Any]:
        """Step 2: Add environmental perspective and compare with economic + Judge assessment"""
        print("Step 2: Adding environmental perspective...")
        
        package = state.input_package
        environmental_cot = package.perspective_specific_cots.get("environmental", "")
        
        # Run comparison analysis for each model
        tasks = [
            self._step2_analysis_claude(state, environmental_cot),
            self._step2_analysis_gpt(state, environmental_cot),
            self._step2_analysis_grok(state, environmental_cot)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        updates = {"step2_complete": True}
        
        # Update existing analyses
        if not isinstance(results[0], Exception) and state.claude_analysis:
            claude_analysis = state.claude_analysis.copy()
            claude_analysis.step2_economic_environmental = results[0]
            claude_analysis.reasoning_evolution.append("Step 2: Environmental comparison completed")
            updates["claude_analysis"] = claude_analysis
            
        if not isinstance(results[1], Exception) and state.gpt_analysis:
            gpt_analysis = state.gpt_analysis.copy()
            gpt_analysis.step2_economic_environmental = results[1]
            gpt_analysis.reasoning_evolution.append("Step 2: Environmental comparison completed")
            updates["gpt_analysis"] = gpt_analysis
            
        if not isinstance(results[2], Exception) and state.grok_analysis:
            grok_analysis = state.grok_analysis.copy()
            grok_analysis.step2_economic_environmental = results[2]
            grok_analysis.reasoning_evolution.append("Step 2: Environmental comparison completed")
            updates["grok_analysis"] = grok_analysis
        
        # Judge assessment of Step 2 results
        print("⚖️ Judge: Step 2 assessment...")
        step2_judge_prompt = f"""
        You are evaluating Step 2 of a multi-perspective analysis where ENVIRONMENTAL perspective was added to ECONOMIC.
        
        ORIGINAL QUERY: {package.query}
        
        STEP 2 ECONOMIC + ENVIRONMENTAL ANALYSES:
        Claude: {results[0] if not isinstance(results[0], Exception) else "Error"}
        GPT: {results[1] if not isinstance(results[1], Exception) else "Error"}
        Grok: {results[2] if not isinstance(results[2], Exception) else "Error"}
        
        STEP 1 CONTEXT:
        Claude Economic: {state.claude_analysis.step1_economic.content if state.claude_analysis and state.claude_analysis.step1_economic else "N/A"}
        GPT Economic: {state.gpt_analysis.step1_economic.content if state.gpt_analysis and state.gpt_analysis.step1_economic else "N/A"}
        Grok Economic: {state.grok_analysis.step1_economic.content if state.grok_analysis and state.grok_analysis.step1_economic else "N/A"}
        
        Assess:
        STEP2_ANALYSIS: [How well did each model integrate environmental with economic perspectives?]
        PERSPECTIVE_CONFLICTS: [What conflicts/tensions emerged between economic and environmental views?]
        SYNTHESIS_QUALITY: [How effectively did models synthesize the two perspectives?]
        READINESS_FOR_TECH: [How prepared are these analyses for technological perspective integration?]
        """
        
        try:
            judge_step2 = await self.judge.judge_client.ainvoke(step2_judge_prompt)
            updates["judge_step2_assessment"] = judge_step2.content
        except Exception as e:
            updates["judge_step2_assessment"] = f"Error in Step 2 judge assessment: {str(e)}"
        
        return updates
    
    async def step3_technological_synthesis_node(self, state: MultiPerspectiveEnsembleState) -> Dict[str, Any]:
        """Step 3: Complete three-perspective synthesis + Judge assessment"""
        print("Step 3: Complete technological synthesis...")
        
        package = state.input_package
        technological_cot = package.perspective_specific_cots.get("technological", "")
        
        # Run final synthesis for each model
        tasks = [
            self._step3_synthesis_claude(state, technological_cot),
            self._step3_synthesis_gpt(state, technological_cot),
            self._step3_synthesis_grok(state, technological_cot)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        updates = {"step3_complete": True}
        
        # Update existing analyses with final synthesis
        if not isinstance(results[0], Exception) and state.claude_analysis:
            claude_analysis = state.claude_analysis.copy()
            claude_analysis.step3_complete_synthesis = results[0]["synthesis"]
            claude_analysis.final_confidence = results[0]["confidence"]
            claude_analysis.reasoning_evolution.append("Step 3: Complete synthesis with technological perspective")
            updates["claude_analysis"] = claude_analysis
            
        if not isinstance(results[1], Exception) and state.gpt_analysis:
            gpt_analysis = state.gpt_analysis.copy()
            gpt_analysis.step3_complete_synthesis = results[1]["synthesis"]
            gpt_analysis.final_confidence = results[1]["confidence"]
            gpt_analysis.reasoning_evolution.append("Step 3: Complete synthesis with technological perspective")
            updates["gpt_analysis"] = gpt_analysis
            
        if not isinstance(results[2], Exception) and state.grok_analysis:
            grok_analysis = state.grok_analysis.copy()
            grok_analysis.step3_complete_synthesis = results[2]["synthesis"]
            grok_analysis.final_confidence = results[2]["confidence"]
            grok_analysis.reasoning_evolution.append("Step 3: Complete synthesis with technological perspective")
            updates["grok_analysis"] = grok_analysis
        
        # Judge assessment of Step 3 results  
        print("Judge: Step 3 assessment...")
        step3_judge_prompt = f"""
        You are evaluating Step 3 of a multi-perspective analysis where TECHNOLOGICAL perspective was integrated with ECONOMIC and ENVIRONMENTAL.
        
        ORIGINAL QUERY: {package.query}
        
        STEP 3 COMPLETE SYNTHESES:
        Claude: {results[0]["synthesis"] if not isinstance(results[0], Exception) else "Error"}
        GPT: {results[1]["synthesis"] if not isinstance(results[1], Exception) else "Error"}  
        Grok: {results[2]["synthesis"] if not isinstance(results[2], Exception) else "Error"}
        
        PREVIOUS STEP CONTEXT:
        Claude Step 2: {state.claude_analysis.step2_economic_environmental if state.claude_analysis else "N/A"}
        GPT Step 2: {state.gpt_analysis.step2_economic_environmental if state.gpt_analysis else "N/A"}
        Grok Step 2: {state.grok_analysis.step2_economic_environmental if state.grok_analysis else "N/A"}
        
        Assess:
        STEP3_ANALYSIS: [How well did each model integrate all three perspectives?]
        COMPREHENSIVE_COVERAGE: [How comprehensively did models address economic, environmental, and technological aspects?]
        SYNTHESIS_SOPHISTICATION: [How sophisticated and nuanced are the final syntheses?]
        READINESS_FOR_FINAL_JUDGMENT: [How ready are these analyses for final comparative evaluation?]
        """
        
        try:
            judge_step3 = await self.judge.judge_client.ainvoke(step3_judge_prompt)
            updates["judge_step3_assessment"] = judge_step3.content
        except Exception as e:
            updates["judge_step3_assessment"] = f"Error in Step 3 judge assessment: {str(e)}"
        
        return updates
    
    async def judge_evaluation_node(self, state: MultiPerspectiveEnsembleState) -> Dict[str, Any]:
        """Final comprehensive judge evaluation synthesizing all analyses and stage assessments"""
        print("Final Judge evaluation and synthesis...")
        
        judge_prompt = self._create_comprehensive_judge_evaluation_prompt(state)
        
        try:
            response = await self.judge.judge_client.ainvoke(judge_prompt)
            content = response.content
            
            # Parse comprehensive judge response
            evaluation = self._extract_judge_section(content, "FINAL_EVALUATION")
            agreements = self._extract_judge_section(content, "AGREEMENTS_DISAGREEMENTS")
            insights = self._extract_judge_section(content, "BEST_INSIGHTS")
            synthesis = self._extract_judge_section(content, "FINAL_SYNTHESIS")
            methodology_assessment = self._extract_judge_section(content, "METHODOLOGY_ASSESSMENT")
            
            # Extract quality scores
            scores = {
                "claude": self._extract_judge_score(content, "CLAUDE_SCORE"),
                "gpt": self._extract_judge_score(content, "GPT_SCORE"),
                "grok": self._extract_judge_score(content, "GROK_SCORE")
            }
            
            return {
                "judge_analysis": evaluation,
                "agreements_disagreements": agreements,
                "best_insights": insights,
                "final_synthesis": synthesis,
                "methodology_assessment": methodology_assessment,
                "quality_scores": scores,
                "judging_complete": True
            }
            
        except Exception as e:
            return {
                "judge_analysis": f"Error in judge evaluation: {str(e)}",
                "final_synthesis": "Unable to complete judge evaluation",
                "judging_complete": True
            }
    
    async def performance_logging_node(self, state: MultiPerspectiveEnsembleState) -> Dict[str, Any]:
        """Enhanced performance comparison: ensemble vs individual baselines with detailed metrics"""
        print("Performance comparison and logging...")
        
        # Comprehensive comparison of ensemble final synthesis against each baseline
        comparison_results = {}
        improvement_metrics = {}
        detailed_analysis = {}
        
        # Collect ensemble results
        ensemble_synthesis = state.final_synthesis or ""
        claude_synthesis = state.claude_analysis.step3_complete_synthesis if state.claude_analysis else ""
        gpt_synthesis = state.gpt_analysis.step3_complete_synthesis if state.gpt_analysis else ""
        grok_synthesis = state.grok_analysis.step3_complete_synthesis if state.grok_analysis else ""
        
        # Detailed comparison metrics
        if state.final_synthesis:
            # Length-based comprehensiveness comparison
            if state.claude_baseline:
                claude_improvement = len(ensemble_synthesis) / max(len(state.claude_baseline.content), 1)
                improvement_metrics["claude_length_improvement"] = min(claude_improvement, 5.0)
                detailed_analysis["claude_baseline_vs_ensemble"] = {
                    "baseline_length": len(state.claude_baseline.content),
                    "ensemble_length": len(ensemble_synthesis),
                    "length_ratio": claude_improvement
                }
                
            if state.gpt_baseline:
                gpt_improvement = len(ensemble_synthesis) / max(len(state.gpt_baseline.content), 1)
                improvement_metrics["gpt_length_improvement"] = min(gpt_improvement, 5.0)
                detailed_analysis["gpt_baseline_vs_ensemble"] = {
                    "baseline_length": len(state.gpt_baseline.content),
                    "ensemble_length": len(ensemble_synthesis),
                    "length_ratio": gpt_improvement
                }
                
            if state.grok_baseline:
                grok_improvement = len(ensemble_synthesis) / max(len(state.grok_baseline.content), 1)
                improvement_metrics["grok_length_improvement"] = min(grok_improvement, 5.0)
                detailed_analysis["grok_baseline_vs_ensemble"] = {
                    "baseline_length": len(state.grok_baseline.content),
                    "ensemble_length": len(ensemble_synthesis),
                    "length_ratio": grok_improvement
                }
        
        # Calculate confidence improvements
        final_confidences = []
        baseline_confidences = []
        
        if state.claude_analysis:
            final_confidences.append(state.claude_analysis.final_confidence)
        if state.gpt_analysis:
            final_confidences.append(state.gpt_analysis.final_confidence)
        if state.grok_analysis:
            final_confidences.append(state.grok_analysis.final_confidence)
            
        if state.claude_baseline:
            baseline_confidences.append(state.claude_baseline.confidence)
        if state.gpt_baseline:
            baseline_confidences.append(state.gpt_baseline.confidence)
        if state.grok_baseline:
            baseline_confidences.append(state.grok_baseline.confidence)
        
        if final_confidences and baseline_confidences:
            avg_final_confidence = sum(final_confidences) / len(final_confidences)
            avg_baseline_confidence = sum(baseline_confidences) / len(baseline_confidences)
            improvement_metrics["confidence_improvement"] = avg_final_confidence - avg_baseline_confidence
            improvement_metrics["average_final_confidence"] = avg_final_confidence
            improvement_metrics["average_baseline_confidence"] = avg_baseline_confidence
        
        # Calculate overall improvement metrics
        if improvement_metrics:
            length_improvements = [v for k, v in improvement_metrics.items() if "length_improvement" in k]
            if length_improvements:
                improvement_metrics["average_length_improvement"] = sum(length_improvements) / len(length_improvements)
        
        # Quality scores analysis
        quality_analysis = {}
        if state.quality_scores:
            quality_analysis = {
                "individual_scores": state.quality_scores,
                "average_quality_score": sum(state.quality_scores.values()) / len(state.quality_scores),
                "best_performing_model": max(state.quality_scores, key=state.quality_scores.get),
                "quality_variance": max(state.quality_scores.values()) - min(state.quality_scores.values())
            }
        
        # Multi-perspective methodology effectiveness
        methodology_effectiveness = {
            "step_completion_rate": sum([
                1 if state.baselines_complete else 0,
                1 if state.step1_complete else 0,
                1 if state.step2_complete else 0,
                1 if state.step3_complete else 0,
                1 if state.judging_complete else 0
            ]) / 5,
            "perspective_integration_success": bool(claude_synthesis and gpt_synthesis and grok_synthesis),
            "judge_involvement_at_each_stage": bool(
                getattr(state, 'judge_initial_assessment', None) and
                getattr(state, 'judge_step1_assessment', None) and
                getattr(state, 'judge_step2_assessment', None) and
                getattr(state, 'judge_step3_assessment', None)
            )
        }
        
        # Log to memory with enhanced structure
        comprehensive_result = {
            "query": state.input_package.query,
            "final_synthesis": ensemble_synthesis,
            "judge_analysis": state.judge_analysis,
            "confidence_scores": state.quality_scores,
            "model_responses": {
                "claude": {
                    "baseline": state.claude_baseline.content if state.claude_baseline else "",
                    "step1_economic": state.claude_analysis.step1_economic.content if state.claude_analysis and state.claude_analysis.step1_economic else "",
                    "step2_economic_environmental": state.claude_analysis.step2_economic_environmental if state.claude_analysis else "",
                    "step3_complete_synthesis": claude_synthesis,
                    "final_confidence": state.claude_analysis.final_confidence if state.claude_analysis else 0.0
                },
                "gpt": {
                    "baseline": state.gpt_baseline.content if state.gpt_baseline else "",
                    "step1_economic": state.gpt_analysis.step1_economic.content if state.gpt_analysis and state.gpt_analysis.step1_economic else "",
                    "step2_economic_environmental": state.gpt_analysis.step2_economic_environmental if state.gpt_analysis else "",
                    "step3_complete_synthesis": gpt_synthesis,
                    "final_confidence": state.gpt_analysis.final_confidence if state.gpt_analysis else 0.0
                },
                "grok": {
                    "baseline": state.grok_baseline.content if state.grok_baseline else "",
                    "step1_economic": state.grok_analysis.step1_economic.content if state.grok_analysis and state.grok_analysis.step1_economic else "",
                    "step2_economic_environmental": state.grok_analysis.step2_economic_environmental if state.grok_analysis else "",
                    "step3_complete_synthesis": grok_synthesis,
                    "final_confidence": state.grok_analysis.final_confidence if state.grok_analysis else 0.0
                }
            },
            "processing_time": state.processing_time,
            "total_iterations": 3,  # Three-step process
            "improvement_metrics": improvement_metrics,
            "methodology_effectiveness": methodology_effectiveness
        }
        
        self.memory_logger.log_result(comprehensive_result)
        
        return {
            "baseline_comparison": detailed_analysis,
            "improvement_metrics": improvement_metrics,
            "quality_analysis": quality_analysis,
            "methodology_effectiveness": methodology_effectiveness,
            "logging_complete": True,
            "performance_summary": f"Multi-perspective approach showed average improvement of {improvement_metrics.get('average_length_improvement', 1.0):.2f}x over baselines"
        }
    
    # Helper methods
    def _create_perspective_prompt(self, query: str, perspective: str, universal_cot: str, specific_cot: str) -> str:
        """Create a perspective-specific prompt with enhanced CoT guidance"""
        
        # Use enhanced CoT if no custom guidance provided
        if not universal_cot:
            universal_cot = self.cot_enhancer.get_universal_cot_guidance()
        if not specific_cot:
            specific_cot = self.cot_enhancer.get_perspective_specific_guidance(perspective)
        
        # Use enhanced multi-perspective CoT prompt
        return self.cot_enhancer.create_multi_perspective_cot_prompt(
            query=query,
            perspective=perspective,
            universal_guidance=universal_cot,
            specific_guidance=specific_cot
        )
    
    async def _get_baseline_claude(self, prompt: str) -> BaselineResponse:
        """Get Claude baseline response"""
        try:
            response = await self.claude_model.client.ainvoke(prompt)
            return BaselineResponse(
                model_type=ModelType.CLAUDE,
                content=response.content,
                confidence=0.5  # Default baseline confidence
            )
        except Exception as e:
            return BaselineResponse(
                model_type=ModelType.CLAUDE,
                content=f"Error: {str(e)}",
                confidence=0.0
            )
    
    async def _get_baseline_gpt(self, prompt: str) -> BaselineResponse:
        """Get GPT baseline response"""
        try:
            response = await self.gpt_model.client.ainvoke(prompt)
            return BaselineResponse(
                model_type=ModelType.GPT,
                content=response.content,
                confidence=0.5
            )
        except Exception as e:
            return BaselineResponse(
                model_type=ModelType.GPT,
                content=f"Error: {str(e)}",
                confidence=0.0
            )
    
    async def _get_baseline_grok(self, prompt: str) -> BaselineResponse:
        """Get Grok baseline response"""
        try:
            response = await self.grok_model.client.chat.completions.create(
                model=self.grok_model.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            return BaselineResponse(
                model_type=ModelType.GROK,
                content=response.choices[0].message.content,
                confidence=0.5
            )
        except Exception as e:
            return BaselineResponse(
                model_type=ModelType.GROK,
                content=f"Error: {str(e)}",
                confidence=0.0
            )
    
    async def _analyze_perspective_claude(self, prompt: str, perspective: Perspective) -> PerspectiveResponse:
        """Analyze perspective using Claude"""
        try:
            response = await self.claude_model.client.ainvoke(prompt)
            content = response.content
            
            analysis = self._extract_section(content, "PERSPECTIVE_ANALYSIS")
            reasoning = self._extract_section(content, "REASONING")
            confidence = self._extract_confidence(content)
            
            return PerspectiveResponse(
                perspective=perspective,
                content=analysis,
                reasoning=reasoning,
                confidence=confidence
            )
        except Exception as e:
            return PerspectiveResponse(
                perspective=perspective,
                content=f"Error: {str(e)}",
                reasoning="Error occurred",
                confidence=0.0
            )
    
    async def _analyze_perspective_gpt(self, prompt: str, perspective: Perspective) -> PerspectiveResponse:
        """Analyze perspective using GPT"""
        try:
            response = await self.gpt_model.client.ainvoke(prompt)
            content = response.content
            
            analysis = self._extract_section(content, "PERSPECTIVE_ANALYSIS")
            reasoning = self._extract_section(content, "REASONING")
            confidence = self._extract_confidence(content)
            
            return PerspectiveResponse(
                perspective=perspective,
                content=analysis,
                reasoning=reasoning,
                confidence=confidence
            )
        except Exception as e:
            return PerspectiveResponse(
                perspective=perspective,
                content=f"Error: {str(e)}",
                reasoning="Error occurred",
                confidence=0.0
            )
    
    async def _analyze_perspective_grok(self, prompt: str, perspective: Perspective) -> PerspectiveResponse:
        """Analyze perspective using Grok"""
        try:
            response = await self.grok_model.client.chat.completions.create(
                model=self.grok_model.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            content = response.choices[0].message.content
            
            analysis = self._extract_section(content, "PERSPECTIVE_ANALYSIS")
            reasoning = self._extract_section(content, "REASONING")
            confidence = self._extract_confidence(content)
            
            return PerspectiveResponse(
                perspective=perspective,
                content=analysis,
                reasoning=reasoning,
                confidence=confidence
            )
        except Exception as e:
            return PerspectiveResponse(
                perspective=perspective,
                content=f"Error: {str(e)}",
                reasoning="Error occurred",
                confidence=0.0
            )
    
    async def _step2_analysis_claude(self, state: MultiPerspectiveEnsembleState, environmental_cot: str) -> str:
        """Claude Step 2: Compare economic and environmental perspectives using enhanced CoT"""
        if not state.claude_analysis or not state.claude_analysis.step1_economic:
            return "No economic analysis available for comparison"
        
        # Use enhanced perspective comparison CoT
        prompt = self.cot_enhancer.create_perspective_comparison_cot_prompt(
            query=state.input_package.query,
            previous_analysis=state.claude_analysis.step1_economic.content,
            previous_perspective="economic",
            new_perspective="environmental",
            guidance=environmental_cot or self.cot_enhancer.get_perspective_specific_guidance("environmental")
        )
        
        try:
            response = await self.claude_model.client.ainvoke(prompt)
            return response.content
        except Exception as e:
            return f"Error in Step 2 analysis: {str(e)}"
    
    async def _step2_analysis_gpt(self, state: MultiPerspectiveEnsembleState, environmental_cot: str) -> str:
        """GPT Step 2: Compare economic and environmental perspectives using enhanced CoT"""
        if not state.gpt_analysis or not state.gpt_analysis.step1_economic:
            return "No economic analysis available for comparison"
        
        # Use enhanced perspective comparison CoT
        prompt = self.cot_enhancer.create_perspective_comparison_cot_prompt(
            query=state.input_package.query,
            previous_analysis=state.gpt_analysis.step1_economic.content,
            previous_perspective="economic",
            new_perspective="environmental",
            guidance=environmental_cot or self.cot_enhancer.get_perspective_specific_guidance("environmental")
        )
        
        try:
            response = await self.gpt_model.client.ainvoke(prompt)
            return response.content
        except Exception as e:
            return f"Error in Step 2 analysis: {str(e)}"
    
    async def _step2_analysis_grok(self, state: MultiPerspectiveEnsembleState, environmental_cot: str) -> str:
        """Grok Step 2: Compare economic and environmental perspectives using enhanced CoT"""
        if not state.grok_analysis or not state.grok_analysis.step1_economic:
            return "No economic analysis available for comparison"
        
        # Use enhanced perspective comparison CoT
        prompt = self.cot_enhancer.create_perspective_comparison_cot_prompt(
            query=state.input_package.query,
            previous_analysis=state.grok_analysis.step1_economic.content,
            previous_perspective="economic",
            new_perspective="environmental",
            guidance=environmental_cot or self.cot_enhancer.get_perspective_specific_guidance("environmental")
        )
        
        try:
            response = await self.grok_model.client.chat.completions.create(
                model=self.grok_model.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in Step 2 analysis: {str(e)}"
    
    async def _step3_synthesis_claude(self, state: MultiPerspectiveEnsembleState, technological_cot: str) -> Dict[str, Any]:
        """Claude Step 3: Complete three-perspective synthesis using enhanced CoT"""
        economic_analysis = state.claude_analysis.step1_economic.content if state.claude_analysis and state.claude_analysis.step1_economic else ""
        environmental_analysis = state.claude_analysis.step2_economic_environmental if state.claude_analysis else ""
        
        # Use enhanced three-perspective synthesis CoT
        prompt = self.cot_enhancer.create_three_perspective_synthesis_cot_prompt(
            query=state.input_package.query,
            economic_analysis=economic_analysis,
            environmental_analysis=environmental_analysis,
            tech_guidance=technological_cot or self.cot_enhancer.get_perspective_specific_guidance("technological")
        )
        
        try:
            response = await self.claude_model.client.ainvoke(prompt)
            content = response.content
            
            synthesis = self._extract_section(content, "COMPREHENSIVE_SYNTHESIS")
            confidence = self._extract_confidence(content)
            
            return {
                "synthesis": synthesis,
                "confidence": confidence
            }
        except Exception as e:
            return {
                "synthesis": f"Error in final synthesis: {str(e)}",
                "confidence": 0.0
            }
    
    async def _step3_synthesis_gpt(self, state: MultiPerspectiveEnsembleState, technological_cot: str) -> Dict[str, Any]:
        """GPT Step 3: Complete three-perspective synthesis using enhanced CoT"""
        economic_analysis = state.gpt_analysis.step1_economic.content if state.gpt_analysis and state.gpt_analysis.step1_economic else ""
        environmental_analysis = state.gpt_analysis.step2_economic_environmental if state.gpt_analysis else ""
        
        # Use enhanced three-perspective synthesis CoT
        prompt = self.cot_enhancer.create_three_perspective_synthesis_cot_prompt(
            query=state.input_package.query,
            economic_analysis=economic_analysis,
            environmental_analysis=environmental_analysis,
            tech_guidance=technological_cot or self.cot_enhancer.get_perspective_specific_guidance("technological")
        )
        
        try:
            response = await self.gpt_model.client.ainvoke(prompt)
            content = response.content
            
            synthesis = self._extract_section(content, "COMPREHENSIVE_SYNTHESIS")
            confidence = self._extract_confidence(content)
            
            return {
                "synthesis": synthesis,
                "confidence": confidence
            }
        except Exception as e:
            return {
                "synthesis": f"Error in final synthesis: {str(e)}",
                "confidence": 0.0
            }
    
    async def _step3_synthesis_grok(self, state: MultiPerspectiveEnsembleState, technological_cot: str) -> Dict[str, Any]:
        """Grok Step 3: Complete three-perspective synthesis using enhanced CoT"""
        economic_analysis = state.grok_analysis.step1_economic.content if state.grok_analysis and state.grok_analysis.step1_economic else ""
        environmental_analysis = state.grok_analysis.step2_economic_environmental if state.grok_analysis else ""
        
        # Use enhanced three-perspective synthesis CoT
        prompt = self.cot_enhancer.create_three_perspective_synthesis_cot_prompt(
            query=state.input_package.query,
            economic_analysis=economic_analysis,
            environmental_analysis=environmental_analysis,
            tech_guidance=technological_cot or self.cot_enhancer.get_perspective_specific_guidance("technological")
        )
        
        try:
            response = await self.grok_model.client.chat.completions.create(
                model=self.grok_model.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            content = response.choices[0].message.content
            
            synthesis = self._extract_section(content, "COMPREHENSIVE_SYNTHESIS")
            confidence = self._extract_confidence(content)
            
            return {
                "synthesis": synthesis,
                "confidence": confidence
            }
        except Exception as e:
            return {
                "synthesis": f"Error in final synthesis: {str(e)}",
                "confidence": 0.0
            }
    
    def _create_comprehensive_judge_evaluation_prompt(self, state: MultiPerspectiveEnsembleState) -> str:
        """Create comprehensive prompt for final judge evaluation incorporating all stage assessments"""
        return f"""
        You are conducting the FINAL COMPREHENSIVE EVALUATION of a sophisticated multi-perspective AI ensemble analysis.
        You have been involved throughout the entire process, providing assessments at each stage.
        
        ORIGINAL QUERY: {state.input_package.query}
        
        === YOUR PREVIOUS STAGE ASSESSMENTS ===
        Initial Assessment: {getattr(state, 'judge_initial_assessment', 'N/A')}
        Step 1 Assessment: {getattr(state, 'judge_step1_assessment', 'N/A')}
        Step 2 Assessment: {getattr(state, 'judge_step2_assessment', 'N/A')}
        Step 3 Assessment: {getattr(state, 'judge_step3_assessment', 'N/A')}
        
        === BASELINE RESPONSES (No Guidance) ===
        Claude Baseline: {state.claude_baseline.content if state.claude_baseline else "N/A"}
        GPT Baseline: {state.gpt_baseline.content if state.gpt_baseline else "N/A"}
        Grok Baseline: {state.grok_baseline.content if state.grok_baseline else "N/A"}
        
        === FINAL MULTI-PERSPECTIVE SYNTHESES ===
        Claude Final Synthesis: {state.claude_analysis.step3_complete_synthesis if state.claude_analysis else "N/A"}
        (Confidence: {state.claude_analysis.final_confidence if state.claude_analysis else 0.0})
        
        GPT Final Synthesis: {state.gpt_analysis.step3_complete_synthesis if state.gpt_analysis else "N/A"}
        (Confidence: {state.gpt_analysis.final_confidence if state.gpt_analysis else 0.0})
        
        Grok Final Synthesis: {state.grok_analysis.step3_complete_synthesis if state.grok_analysis else "N/A"}
        (Confidence: {state.grok_analysis.final_confidence if state.grok_analysis else 0.0})
        
        === REASONING EVOLUTION TRACKING ===
        Claude Evolution: {state.claude_analysis.reasoning_evolution if state.claude_analysis else []}
        GPT Evolution: {state.gpt_analysis.reasoning_evolution if state.gpt_analysis else []}
        Grok Evolution: {state.grok_analysis.reasoning_evolution if state.grok_analysis else []}
        
        Based on your comprehensive involvement throughout this process, provide your FINAL evaluation:
        
        FINAL_EVALUATION: [Your comprehensive evaluation of the entire multi-perspective process and final results]
        
        AGREEMENTS_DISAGREEMENTS: [Key agreements and disagreements between models across all stages]
        
        BEST_INSIGHTS: [The most valuable insights extracted from the entire process]
        
        FINAL_SYNTHESIS: [Your ultimate synthesized answer that represents the best possible response to the original query]
        
        METHODOLOGY_ASSESSMENT: [Evaluation of the multi-perspective methodology's effectiveness vs simple baseline responses]
        
        CLAUDE_SCORE: [0.0-1.0 - considering entire process, not just final result]
        GPT_SCORE: [0.0-1.0 - considering entire process, not just final result]
        GROK_SCORE: [0.0-1.0 - considering entire process, not just final result]
        """
    
    def _create_judge_evaluation_prompt(self, state: MultiPerspectiveEnsembleState) -> str:
        """Create prompt for judge evaluation"""
        return f"""
        You are an expert judge evaluating multi-perspective AI analyses. 
        
        ORIGINAL QUERY: {state.input_package.query}
        
        BASELINE RESPONSES (No Guidance):
        Claude Baseline: {state.claude_baseline.content if state.claude_baseline else "N/A"}
        GPT Baseline: {state.gpt_baseline.content if state.gpt_baseline else "N/A"}
        Grok Baseline: {state.grok_baseline.content if state.grok_baseline else "N/A"}
        
        MULTI-PERSPECTIVE ANALYSES:
        
        Claude Analysis:
        - Economic: {state.claude_analysis.step1_economic.content if state.claude_analysis and state.claude_analysis.step1_economic else "N/A"}
        - Economic+Environmental: {state.claude_analysis.step2_economic_environmental if state.claude_analysis else "N/A"}
        - Complete Synthesis: {state.claude_analysis.step3_complete_synthesis if state.claude_analysis else "N/A"}
        
        GPT Analysis:
        - Economic: {state.gpt_analysis.step1_economic.content if state.gpt_analysis and state.gpt_analysis.step1_economic else "N/A"}
        - Economic+Environmental: {state.gpt_analysis.step2_economic_environmental if state.gpt_analysis else "N/A"}
        - Complete Synthesis: {state.gpt_analysis.step3_complete_synthesis if state.gpt_analysis else "N/A"}
        
        Grok Analysis:
        - Economic: {state.grok_analysis.step1_economic.content if state.grok_analysis and state.grok_analysis.step1_economic else "N/A"}
        - Economic+Environmental: {state.grok_analysis.step2_economic_environmental if state.grok_analysis else "N/A"}
        - Complete Synthesis: {state.grok_analysis.step3_complete_synthesis if state.grok_analysis else "N/A"}
        
        Please provide:
        
        EVALUATION: [Detailed evaluation of each model's multi-perspective analysis]
        AGREEMENTS_DISAGREEMENTS: [Key points of agreement and disagreement between models]
        BEST_INSIGHTS: [The best insights extracted from all analyses]
        FINAL_SYNTHESIS: [Your final synthesized answer incorporating the best from all models]
        
        CLAUDE_SCORE: [0.0-1.0]
        GPT_SCORE: [0.0-1.0]
        GROK_SCORE: [0.0-1.0]
        """
    
    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a specific section from the response"""
        try:
            lines = content.split('\n')
            section_content = []
            capturing = False
            
            for line in lines:
                if line.strip().startswith(f"{section_name}:"):
                    capturing = True
                    section_content.append(line.split(':', 1)[1].strip())
                elif capturing and any(line.strip().startswith(f"{s}:") for s in 
                    ["PERSPECTIVE_ANALYSIS", "REASONING", "CONFIDENCE", "ENVIRONMENTAL_ANALYSIS", 
                     "COMPARISON", "SYNTHESIS", "TECHNOLOGICAL_ANALYSIS", "COMPLETE_SYNTHESIS", "FINAL_CONFIDENCE"]):
                    break
                elif capturing:
                    section_content.append(line)
            
            return '\n'.join(section_content).strip()
        except:
            return content
    
    def _extract_confidence(self, content: str) -> float:
        """Extract confidence score from response"""
        try:
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith('CONFIDENCE:') or line.strip().startswith('FINAL_CONFIDENCE:'):
                    confidence_str = line.split(':', 1)[1].strip()
                    return float(confidence_str)
            return 0.7  # Default confidence
        except:
            return 0.7
    
    def _extract_judge_section(self, content: str, section_name: str) -> str:
        """Extract a section from judge response"""
        try:
            lines = content.split('\n')
            section_content = []
            capturing = False
            
            for line in lines:
                if line.strip().startswith(f"{section_name}:"):
                    capturing = True
                    section_content.append(line.split(':', 1)[1].strip())
                elif capturing and any(line.strip().startswith(f"{s}:") for s in 
                    ["EVALUATION", "AGREEMENTS_DISAGREEMENTS", "BEST_INSIGHTS", "FINAL_SYNTHESIS", 
                     "CLAUDE_SCORE", "GPT_SCORE", "GROK_SCORE"]):
                    break
                elif capturing:
                    section_content.append(line)
            
            return '\n'.join(section_content).strip()
        except:
            return content
    
    def _extract_judge_score(self, content: str, score_name: str) -> float:
        """Extract a score from judge response"""
        try:
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith(f"{score_name}:"):
                    score_str = line.split(':', 1)[1].strip()
                    return max(0.0, min(1.0, float(score_str)))
            return 0.5  # Default score
        except:
            return 0.5
