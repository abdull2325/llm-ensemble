#!/usr/bin/env python3
"""
Enhanced Multi-Perspective LLM Ensemble System

A sophisticated system that analyzes queries through multiple perspectives
(economic, environmental, technological) using both universal and perspective-specific
Chain of Thought instructions, with comprehensive performance comparison against baselines.
"""

import asyncio
import sys
from typing import Dict, Any
from graph.multi_perspective_ensemble_graph import MultiPerspectiveEnsembleGraph
from utils.memory import MemoryLogger
from config.settings import settings

class EnhancedLLMEnsembleSystem:
    """Enhanced Multi-Perspective LLM Ensemble System"""
    
    def __init__(self):
        """Initialize the enhanced ensemble system"""
        try:
            # Validate API keys
            settings.validate_api_keys()
            
            # Initialize components
            self.ensemble_graph = MultiPerspectiveEnsembleGraph()
            self.memory_logger = MemoryLogger("multi_perspective_memory.json")
            
            print(" Enhanced Multi-Perspective LLM Ensemble System initialized!")
            print(" Perspectives: Economic, Environmental, Technological")
            print(" Chain of Thought: Universal + Perspective-specific")
            print(" Performance: Multi-step analysis vs baseline comparison")
            
        except Exception as e:
            print(f" Error initializing enhanced system: {e}")
            sys.exit(1)
    
    def validate_inputs(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Validate and prepare inputs for multi-perspective analysis
        
        Expected format from user:
        - query: The main question
        - perspective_1, perspective_2, perspective_3: Analytical dimensions
        - universal_cot: Universal chain of thought guidance
        - chain_of_thought_1, chain_of_thought_2, chain_of_thought_3: Perspective-specific CoTs
        """
        
        if not query or not query.strip():
            raise ValueError("Query is required and cannot be empty")
        
        # Extract perspectives (with defaults)
        perspective_1 = kwargs.get("perspective_1", "economic")
        perspective_2 = kwargs.get("perspective_2", "environmental") 
        perspective_3 = kwargs.get("perspective_3", "technological")
        
        # Extract CoT instructions (optional)
        universal_cot = kwargs.get("universal_cot", "")
        chain_of_thought_1 = kwargs.get("chain_of_thought_1", "")
        chain_of_thought_2 = kwargs.get("chain_of_thought_2", "")
        chain_of_thought_3 = kwargs.get("chain_of_thought_3", "")
        
        validated_package = {
            "query": query.strip(),
            "perspective_1": perspective_1,
            "perspective_2": perspective_2,
            "perspective_3": perspective_3,
            "universal_cot": universal_cot,
            "chain_of_thought_1": chain_of_thought_1,
            "chain_of_thought_2": chain_of_thought_2,
            "chain_of_thought_3": chain_of_thought_3
        }
        
        print(" Input validation successful!")
        print(f" Query: {query[:100]}...")
        print(f" Perspectives: {perspective_1}, {perspective_2}, {perspective_3}")
        
        if universal_cot:
            print(f" Universal CoT: {universal_cot[:50]}...")
        
        perspective_cots = [chain_of_thought_1, chain_of_thought_2, chain_of_thought_3]
        cot_count = len([cot for cot in perspective_cots if cot.strip()])
        print(f"Perspective-specific CoTs: {cot_count}/3 provided")
        
        return validated_package
    
    async def process_multi_perspective_query(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Process a query through the enhanced multi-perspective ensemble system
        
        This implements the complete workflow:
        1. Baseline responses (raw, no guidance)
        2. Step 1: Single perspective (economic)
        3. Step 2: Two perspectives (economic + environmental) 
        4. Step 3: Complete analysis (economic + environmental + technological)
        5. Judge evaluation and synthesis
        6. Performance comparison against baselines
        """
        
        print(f"\n Processing Multi-Perspective Query: {query}")
        
        try:
            # Validate inputs
            validated_inputs = self.validate_inputs(query, **kwargs)
            
            # Process through the ensemble graph
            result = await self.ensemble_graph.process_multi_perspective_query(**validated_inputs)
            
            # Log the comprehensive result
            self.memory_logger.log_result(result)
            
            return result
            
        except Exception as e:
            error_result = {
                "query": query,
                "error": str(e),
                "processing_time": 0.0,
                "completion_status": "failed"
            }
            print(f" Error processing multi-perspective query: {e}")
            return error_result
    
    def analyze_performance_improvement(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze how much the multi-perspective approach improved over baselines"""
        
        if "error" in result:
            return {"analysis": "Cannot analyze performance due to processing error"}
        
        performance = result.get("performance_comparison", {})
        improvement_metrics = performance.get("improvement_metrics", {})
        advantage_metrics = performance.get("multi_perspective_advantage", {})
        
        analysis = {
            "baseline_vs_ensemble_comparison": {},
            "multi_perspective_advantages": {},
            "summary": ""
        }
        
        # Analyze improvement metrics
        if improvement_metrics:
            analysis["baseline_vs_ensemble_comparison"] = improvement_metrics
            
            avg_improvement = improvement_metrics.get("average_improvement", 1.0)
            if avg_improvement > 1.2:
                improvement_level = "Significant"
            elif avg_improvement > 1.05:
                improvement_level = "Moderate" 
            else:
                improvement_level = "Minimal"
                
            analysis["summary"] += f"{improvement_level} improvement over baselines. "
        
        # Analyze multi-perspective advantages
        if advantage_metrics:
            analysis["multi_perspective_advantages"] = advantage_metrics
            
            comprehensiveness = advantage_metrics.get("comprehensiveness_improvement", 1.0)
            confidence = advantage_metrics.get("confidence_improvement", 0.0)
            
            if comprehensiveness > 1.5:
                analysis["summary"] += "Multi-perspective approach significantly more comprehensive. "
            if confidence > 0.1:
                analysis["summary"] += "Notable confidence improvement through multi-step analysis."
        
        return analysis
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics from memory"""
        return self.memory_logger.get_performance_stats()
    
    def get_best_model_by_perspective(self) -> Dict[str, Any]:
        """Analyze which model performs best for each perspective"""
        # This would analyze historical data to determine model strengths
        # For now, return placeholder
        return {
            "economic_perspective": "Analysis would require historical data",
            "environmental_perspective": "Analysis would require historical data", 
            "technological_perspective": "Analysis would require historical data"
        }

def print_multi_perspective_result(result: Dict[str, Any]):
    """Pretty print the multi-perspective ensemble result"""
    print("\n" + "="*100)
    print(" MULTI-PERSPECTIVE LLM ENSEMBLE RESULT")
    print("="*100)
    
    if "error" in result:
        print(f" Error: {result['error']}")
        return
    
    print(f" Query: {result['query']}")
    print(f"⏱ Processing Time: {result.get('processing_time', 0):.2f} seconds")
    
    # Show completion status
    status = result.get('completion_status', {})
    print(f"\n Completion Status:")
    for step, completed in status.items():
        emoji = "✅" if completed else "❌"
        print(f"  {emoji} {step.replace('_', ' ').title()}")
    
    # Show input configuration
    input_pkg = result.get('input_package', {})
    print(f"\n Analysis Configuration:")
    print(f"  Perspectives: {', '.join(input_pkg.get('perspectives', []))}")
    if input_pkg.get('universal_cot'):
        print(f"  Universal CoT: {input_pkg['universal_cot'][:100]}...")
    
    # Show judge evaluation
    judge = result.get('judge_analysis', {})
    print(f"\n JUDGE FINAL SYNTHESIS:")
    print("-" * 50)
    print(judge.get('final_synthesis', 'No synthesis available')[:500] + "...")
    
    # Show quality scores
    scores = judge.get('quality_scores', {})
    if scores:
        print(f"\n Quality Scores:")
        for model, score in scores.items():
            print(f"  {model.upper()}: {score:.3f}")
    
    # Show performance comparison
    performance = result.get('performance_comparison', {})
    improvement = performance.get('improvement_metrics', {})
    if improvement:
        print(f"\n Performance vs Baselines:")
        avg_improvement = improvement.get('average_improvement', 1.0)
        print(f"  Average Improvement: {avg_improvement:.2f}x")
        
        advantage = performance.get('multi_perspective_advantage', {})
        if advantage:
            comp_improvement = advantage.get('comprehensiveness_improvement', 1.0)
            conf_improvement = advantage.get('confidence_improvement', 0.0)
            print(f"  Comprehensiveness: {comp_improvement:.2f}x")
            print(f"  Confidence Boost: +{conf_improvement:.3f}")

async def main():
    """Main function for command-line usage"""
    
    # Example usage showing the expected input format
    if len(sys.argv) < 2:
        print("Usage: python multi_perspective_main.py '<query>' [options]")
        print("\nExample:")
        print('python multi_perspective_main.py "What are the benefits of renewable energy?" \\')
        print('  --universal_cot "be concise, focus on ground truth research" \\')
        print('  --chain_of_thought_1 "consider costs over next 30 years" \\')
        print('  --chain_of_thought_2 "consider health effects over next 30 years"')
        sys.exit(1)
    
    # Parse command line arguments (simplified)
    query = sys.argv[1]
    kwargs = {}
    
    # Simple argument parsing
    i = 2
    while i < len(sys.argv):
        if sys.argv[i].startswith('--') and i + 1 < len(sys.argv):
            key = sys.argv[i][2:]  # Remove --
            value = sys.argv[i + 1]
            kwargs[key] = value
            i += 2
        else:
            i += 1
    
    # Initialize the enhanced system
    ensemble = EnhancedLLMEnsembleSystem()
    
    # Process the query
    result = await ensemble.process_multi_perspective_query(query, **kwargs)
    
    # Print the result
    print_multi_perspective_result(result)
    
    # Show performance analysis
    performance_analysis = ensemble.analyze_performance_improvement(result)
    print(f"\n🔬 Performance Analysis:")
    print(f"Summary: {performance_analysis.get('summary', 'No analysis available')}")

if __name__ == "__main__":
    asyncio.run(main())
