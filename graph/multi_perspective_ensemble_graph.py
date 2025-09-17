from langgraph.graph import StateGraph, END
from graph.multi_perspective_state import MultiPerspectiveEnsembleState, InputPackage
from graph.multi_perspective_nodes import MultiPerspectiveNodes
from typing import Dict, Any
import time

class MultiPerspectiveEnsembleGraph:
    """Enhanced LangGraph workflow for multi-perspective ensemble analysis"""
    
    def __init__(self):
        self.nodes = MultiPerspectiveNodes()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the multi-perspective LangGraph workflow"""
        
        # Create the state graph
        workflow = StateGraph(MultiPerspectiveEnsembleState)
        
        # Add nodes for the multi-perspective workflow
        workflow.add_node("baseline_analysis", self.nodes.baseline_analysis_node)
        workflow.add_node("step1_economic", self.nodes.step1_economic_analysis_node)
        workflow.add_node("step2_environmental", self.nodes.step2_environmental_analysis_node)
        workflow.add_node("step3_technological", self.nodes.step3_technological_synthesis_node)
        workflow.add_node("judge_evaluation", self.nodes.judge_evaluation_node)
        workflow.add_node("performance_logging", self.nodes.performance_logging_node)
        
        # Set entry point
        workflow.set_entry_point("baseline_analysis")
        
        # Add sequential edges for the multi-step analysis
        workflow.add_edge("baseline_analysis", "step1_economic")
        workflow.add_edge("step1_economic", "step2_environmental")
        workflow.add_edge("step2_environmental", "step3_technological")
        workflow.add_edge("step3_technological", "judge_evaluation")
        workflow.add_edge("judge_evaluation", "performance_logging")
        workflow.add_edge("performance_logging", END)
        
        return workflow.compile()
    
    def validate_and_prepare_inputs(self, query: str, perspective_1: str = "economic", 
                                  perspective_2: str = "environmental", perspective_3: str = "technological",
                                  universal_cot: str = "", **perspective_cots) -> InputPackage:
        """Validate and prepare inputs for the ensemble analysis"""
        
        # Create perspective-specific CoTs dictionary
        perspective_specific_cots = {
            perspective_1: perspective_cots.get("chain_of_thought_1", ""),
            perspective_2: perspective_cots.get("chain_of_thought_2", ""),
            perspective_3: perspective_cots.get("chain_of_thought_3", "")
        }
        
        # Create input package
        input_package = InputPackage(
            query=query,
            perspective_1=perspective_1,
            perspective_2=perspective_2,
            perspective_3=perspective_3,
            universal_cot=universal_cot,
            perspective_specific_cots=perspective_specific_cots
        )
        
        # Validate inputs
        input_package.validate_inputs()
        
        print("✅ Input package validated and prepared:")
        print(f"📝 Query: {query}")
        print(f"🔍 Perspectives: {perspective_1}, {perspective_2}, {perspective_3}")
        print(f"🧠 Universal CoT: {'✓' if universal_cot else '✗'}")
        print(f"🎯 Perspective CoTs: {len([v for v in perspective_specific_cots.values() if v])}/3 provided")
        
        return input_package
    
    async def process_multi_perspective_query(self, query: str, perspective_1: str = "economic",
                                            perspective_2: str = "environmental", perspective_3: str = "technological",
                                            universal_cot: str = "", chain_of_thought_1: str = "",
                                            chain_of_thought_2: str = "", chain_of_thought_3: str = "") -> Dict[str, Any]:
        """
        Process a query through the multi-perspective ensemble system
        
        Args:
            query: The main question to analyze
            perspective_1: First analytical perspective (default: economic)
            perspective_2: Second analytical perspective (default: environmental)
            perspective_3: Third analytical perspective (default: technological)
            universal_cot: Universal chain of thought guidance applied to all perspectives
            chain_of_thought_1: Specific CoT for perspective 1
            chain_of_thought_2: Specific CoT for perspective 2
            chain_of_thought_3: Specific CoT for perspective 3
        """
        start_time = time.time()
        
        # Validate and prepare inputs
        try:
            input_package = self.validate_and_prepare_inputs(
                query=query,
                perspective_1=perspective_1,
                perspective_2=perspective_2,
                perspective_3=perspective_3,
                universal_cot=universal_cot,
                chain_of_thought_1=chain_of_thought_1,
                chain_of_thought_2=chain_of_thought_2,
                chain_of_thought_3=chain_of_thought_3
            )
        except Exception as e:
            return {
                "error": f"Input validation failed: {str(e)}",
                "query": query,
                "processing_time": time.time() - start_time
            }
        
        # Initialize state
        initial_state = MultiPerspectiveEnsembleState(
            input_package=input_package
        )
        
        print(f"\n🚀 Starting Multi-Perspective LLM Ensemble Analysis...")
        print(f"📊 Query: {query[:100]}...")
        
        try:
            # Run the graph
            final_state = await self.graph.ainvoke(initial_state)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Prepare comprehensive result
            result = {
                "query": query,
                "input_package": {
                    "perspectives": [perspective_1, perspective_2, perspective_3],
                    "universal_cot": universal_cot,
                    "perspective_cots": input_package.perspective_specific_cots
                },
                
                # Baseline responses
                "baseline_responses": {
                    "claude": {
                        "content": final_state.get("claude_baseline").content if final_state.get("claude_baseline") else "",
                        "confidence": final_state.get("claude_baseline").confidence if final_state.get("claude_baseline") else 0.0
                    },
                    "gpt": {
                        "content": final_state.get("gpt_baseline").content if final_state.get("gpt_baseline") else "",
                        "confidence": final_state.get("gpt_baseline").confidence if final_state.get("gpt_baseline") else 0.0
                    },
                    "grok": {
                        "content": final_state.get("grok_baseline").content if final_state.get("grok_baseline") else "",
                        "confidence": final_state.get("grok_baseline").confidence if final_state.get("grok_baseline") else 0.0
                    }
                },
                
                # Multi-perspective analyses
                "multi_perspective_analyses": {
                    "claude": {
                        "step1_economic": final_state.get("claude_analysis").step1_economic.content if final_state.get("claude_analysis") and final_state.get("claude_analysis").step1_economic else "",
                        "step2_economic_environmental": final_state.get("claude_analysis").step2_economic_environmental if final_state.get("claude_analysis") else "",
                        "step3_complete_synthesis": final_state.get("claude_analysis").step3_complete_synthesis if final_state.get("claude_analysis") else "",
                        "final_confidence": final_state.get("claude_analysis").final_confidence if final_state.get("claude_analysis") else 0.0,
                        "reasoning_evolution": final_state.get("claude_analysis").reasoning_evolution if final_state.get("claude_analysis") else []
                    },
                    "gpt": {
                        "step1_economic": final_state.get("gpt_analysis").step1_economic.content if final_state.get("gpt_analysis") and final_state.get("gpt_analysis").step1_economic else "",
                        "step2_economic_environmental": final_state.get("gpt_analysis").step2_economic_environmental if final_state.get("gpt_analysis") else "",
                        "step3_complete_synthesis": final_state.get("gpt_analysis").step3_complete_synthesis if final_state.get("gpt_analysis") else "",
                        "final_confidence": final_state.get("gpt_analysis").final_confidence if final_state.get("gpt_analysis") else 0.0,
                        "reasoning_evolution": final_state.get("gpt_analysis").reasoning_evolution if final_state.get("gpt_analysis") else []
                    },
                    "grok": {
                        "step1_economic": final_state.get("grok_analysis").step1_economic.content if final_state.get("grok_analysis") and final_state.get("grok_analysis").step1_economic else "",
                        "step2_economic_environmental": final_state.get("grok_analysis").step2_economic_environmental if final_state.get("grok_analysis") else "",
                        "step3_complete_synthesis": final_state.get("grok_analysis").step3_complete_synthesis if final_state.get("grok_analysis") else "",
                        "final_confidence": final_state.get("grok_analysis").final_confidence if final_state.get("grok_analysis") else 0.0,
                        "reasoning_evolution": final_state.get("grok_analysis").reasoning_evolution if final_state.get("grok_analysis") else []
                    }
                },
                
                # Judge evaluation with stage assessments
                "judge_evaluation": {
                    "initial_assessment": final_state.get("judge_initial_assessment", ""),
                    "step1_assessment": final_state.get("judge_step1_assessment", ""),
                    "step2_assessment": final_state.get("judge_step2_assessment", ""),
                    "step3_assessment": final_state.get("judge_step3_assessment", ""),
                    "final_evaluation": final_state.get("judge_analysis", ""),
                    "agreements_disagreements": final_state.get("agreements_disagreements", ""),
                    "best_insights": final_state.get("best_insights", ""),
                    "final_synthesis": final_state.get("final_synthesis", ""),
                    "methodology_assessment": final_state.get("methodology_assessment", ""),
                    "quality_scores": final_state.get("quality_scores", {})
                },
                
                # Enhanced performance comparison
                "performance_comparison": {
                    "baseline_comparison": final_state.get("baseline_comparison", {}),
                    "improvement_metrics": final_state.get("improvement_metrics", {}),
                    "quality_analysis": final_state.get("quality_analysis", {}),
                    "methodology_effectiveness": final_state.get("methodology_effectiveness", {}),
                    "multi_perspective_advantage": self._calculate_advantage_metrics(final_state)
                },
                
                # Metadata
                "processing_time": processing_time,
                "completion_status": {
                    "baselines_complete": final_state.get("baselines_complete", False),
                    "step1_complete": final_state.get("step1_complete", False),
                    "step2_complete": final_state.get("step2_complete", False),
                    "step3_complete": final_state.get("step3_complete", False),
                    "judging_complete": final_state.get("judging_complete", False),
                    "logging_complete": final_state.get("logging_complete", False)
                }
            }
            
            print(f"Multi-perspective analysis is completed in {processing_time:.2f} seconds")
            return result
            
        except Exception as e:
            print(f"Error during multi-perspective processing: {str(e)}")
            return {
                "query": query,
                "error": str(e),
                "processing_time": time.time() - start_time,
                "completion_status": "failed"
            }
    
    def _calculate_advantage_metrics(self, final_state) -> Dict[str, Any]:
        """Calculate metrics showing the advantage of multi-perspective approach"""
        metrics = {}
        
        # Compare synthesis lengths (proxy for comprehensiveness)
        synthesis_lengths = []
        baseline_lengths = []
        
        if final_state.get("claude_analysis") and final_state.get("claude_analysis").step3_complete_synthesis:
            synthesis_lengths.append(len(final_state.get("claude_analysis").step3_complete_synthesis))
        if final_state.get("gpt_analysis") and final_state.get("gpt_analysis").step3_complete_synthesis:
            synthesis_lengths.append(len(final_state.get("gpt_analysis").step3_complete_synthesis))
        if final_state.get("grok_analysis") and final_state.get("grok_analysis").step3_complete_synthesis:
            synthesis_lengths.append(len(final_state.get("grok_analysis").step3_complete_synthesis))
        
        if final_state.get("claude_baseline"):
            baseline_lengths.append(len(final_state.get("claude_baseline").content))
        if final_state.get("gpt_baseline"):
            baseline_lengths.append(len(final_state.get("gpt_baseline").content))
        if final_state.get("grok_baseline"):
            baseline_lengths.append(len(final_state.get("grok_baseline").content))
        
        if synthesis_lengths and baseline_lengths:
            avg_synthesis_length = sum(synthesis_lengths) / len(synthesis_lengths)
            avg_baseline_length = sum(baseline_lengths) / len(baseline_lengths)
            
            metrics["comprehensiveness_improvement"] = avg_synthesis_length / max(avg_baseline_length, 1)
            metrics["average_synthesis_length"] = avg_synthesis_length
            metrics["average_baseline_length"] = avg_baseline_length
        
        # Calculate confidence improvements
        final_confidences = []
        if final_state.get("claude_analysis"):
            final_confidences.append(final_state.get("claude_analysis").final_confidence)
        if final_state.get("gpt_analysis"):
            final_confidences.append(final_state.get("gpt_analysis").final_confidence)
        if final_state.get("grok_analysis"):
            final_confidences.append(final_state.get("grok_analysis").final_confidence)
        
        baseline_confidences = [0.5, 0.5, 0.5]  # Default baseline confidence
        
        if final_confidences:
            avg_final_confidence = sum(final_confidences) / len(final_confidences)
            avg_baseline_confidence = sum(baseline_confidences) / len(baseline_confidences)
            
            metrics["confidence_improvement"] = avg_final_confidence - avg_baseline_confidence
            metrics["average_final_confidence"] = avg_final_confidence
        
        return metrics
