#!/usr/bin/env python3
"""
Enhanced Multi-Perspective LLM Ensemble Demonstration
Showcasing the improved system with judge involvement at each stage
"""

import asyncio
import time
from graph.multi_perspective_ensemble_graph import MultiPerspectiveEnsembleGraph
from utils.chain_of_thought import ChainOfThoughtEnhancer

async def demonstrate_enhanced_multi_perspective_analysis():
    """Demonstrate the enhanced multi-perspective analysis with judge involvement at each stage"""
    
    print(" Enhanced Multi-Perspective LLM Ensemble Demonstration")
    print("=" * 80)
    
    # Initialize the enhanced ensemble graph
    ensemble = MultiPerspectiveEnsembleGraph()
    cot_enhancer = ChainOfThoughtEnhancer()
    
    # Example query about renewable energy (perfect for economic, environmental, technological analysis)
    query = """
    What are the benefits and challenges of implementing large-scale solar energy projects 
    in developing countries, and how can these projects be made financially viable while 
    ensuring environmental sustainability and technological advancement?
    """
    
    print(f"Query: {query}")
    print("\n" + "=" * 80)
    
    # Enhanced universal and perspective-specific guidance
    universal_cot = cot_enhancer.get_universal_cot_guidance()
    economic_cot = cot_enhancer.get_perspective_specific_guidance("economic")
    environmental_cot = cot_enhancer.get_perspective_specific_guidance("environmental")
    technological_cot = cot_enhancer.get_perspective_specific_guidance("technological")
    
    print("Enhanced Chain of Thought Guidance:")
    print(f"Universal CoT: {len(universal_cot)} characters")
    print(f"Economic CoT: {len(economic_cot)} characters")
    print(f"Environmental CoT: {len(environmental_cot)} characters")
    print(f"Technological CoT: {len(technological_cot)} characters")
    print("\n" + "=" * 80)
    
    start_time = time.time()
    
    try:
        # Run the enhanced multi-perspective analysis
        result = await ensemble.process_multi_perspective_query(
            query=query,
            perspective_1="economic",
            perspective_2="environmental", 
            perspective_3="technological",
            universal_cot=universal_cot,
            chain_of_thought_1=economic_cot,
            chain_of_thought_2=environmental_cot,
            chain_of_thought_3=technological_cot
        )
        
        processing_time = time.time() - start_time
        
        print(f"Analysis completed in {processing_time:.2f} seconds")
        print("\n" + "=" * 80)
        
        # Display comprehensive results
        print(" ENHANCED MULTI-PERSPECTIVE ANALYSIS RESULTS")
        print("=" * 80)
        
        # Completion Status
        print("\n PROCESS COMPLETION STATUS:")
        completion = result.get("completion_status", {})
        for stage, completed in completion.items():
            status = "✅" if completed else "❌"
            print(f"  {status} {stage.replace('_', ' ').title()}")
        
        # Judge Assessments at Each Stage
        print("\n JUDGE ASSESSMENTS AT EACH STAGE:")
        judge_eval = result.get("judge_evaluation", {})
        
        if judge_eval.get("initial_assessment"):
            print(" Initial Assessment:")
            print(f"  {judge_eval['initial_assessment'][:200]}...")
            
        if judge_eval.get("step1_assessment"):
            print("\n Step 1 (Economic) Assessment:")
            print(f"  {judge_eval['step1_assessment'][:200]}...")
            
        if judge_eval.get("step2_assessment"):
            print("\n Step 2 (Environmental) Assessment:")
            print(f"  {judge_eval['step2_assessment'][:200]}...")
            
        if judge_eval.get("step3_assessment"):
            print("\n Step 3 (Technological) Assessment:")
            print(f"  {judge_eval['step3_assessment'][:200]}...")
        
        # Baseline vs Multi-Perspective Comparison
        print("\n BASELINE vs MULTI-PERSPECTIVE COMPARISON:")
        baselines = result.get("baseline_responses", {})
        multi_perspective = result.get("multi_perspective_analyses", {})
        
        for model in ["claude", "gpt", "grok"]:
            baseline_length = len(baselines.get(model, {}).get("content", ""))
            synthesis_length = len(multi_perspective.get(model, {}).get("step3_complete_synthesis", ""))
            improvement = synthesis_length / max(baseline_length, 1) if baseline_length > 0 else 0
            
            print(f"  {model.upper()}:")
            print(f"    Baseline: {baseline_length} chars")
            print(f"    Final Synthesis: {synthesis_length} chars")
            print(f"    Improvement: {improvement:.2f}x")
        
        # Quality Scores
        print("\n QUALITY SCORES FROM JUDGE:")
        quality_scores = judge_eval.get("quality_scores", {})
        if quality_scores:
            best_model = max(quality_scores, key=quality_scores.get)
            print(f"   Best Performing: {best_model.upper()} ({quality_scores[best_model]:.3f})")
            for model, score in quality_scores.items():
                print(f"    {model.upper()}: {score:.3f}")
        
        # Final Synthesis
        print("\n FINAL JUDGE SYNTHESIS:")
        final_synthesis = judge_eval.get("final_synthesis", "")
        if final_synthesis:
            print(f"  {final_synthesis[:500]}...")
        
        # Methodology Assessment
        print("\n🔬 METHODOLOGY EFFECTIVENESS:")
        methodology = judge_eval.get("methodology_assessment", "")
        if methodology:
            print(f"  {methodology[:300]}...")
        
        # Performance Metrics
        print("\n PERFORMANCE METRICS:")
        performance = result.get("performance_comparison", {})
        improvement_metrics = performance.get("improvement_metrics", {})
        methodology_effectiveness = performance.get("methodology_effectiveness", {})
        
        if improvement_metrics:
            avg_improvement = improvement_metrics.get("average_length_improvement", 1.0)
            confidence_improvement = improvement_metrics.get("confidence_improvement", 0.0)
            print(f"   Average Length Improvement: {avg_improvement:.2f}x")
            print(f"   Confidence Improvement: {confidence_improvement:+.3f}")
        
        if methodology_effectiveness:
            completion_rate = methodology_effectiveness.get("step_completion_rate", 0.0)
            judge_involvement = methodology_effectiveness.get("judge_involvement_at_each_stage", False)
            print(f"   Step Completion Rate: {completion_rate:.1%}")
            print(f"   Judge Involvement at Each Stage: {'Yes' if judge_involvement else 'No'}")
        
        # Key Insights
        print("\n KEY INSIGHTS:")
        best_insights = judge_eval.get("best_insights", "")
        if best_insights:
            print(f"  {best_insights[:400]}...")
        
        # Agreements and Disagreements
        print("\n AGREEMENTS & DISAGREEMENTS:")
        agreements = judge_eval.get("agreements_disagreements", "")
        if agreements:
            print(f"  {agreements[:300]}...")
        
        print("\n" + "=" * 80)
        print(" Enhanced Multi-Perspective Analysis Complete!")
        print(f" Total Processing Time: {processing_time:.2f} seconds")
        print(f" Multi-Stage Process with Judge Oversight: Complete")
        print(f" Performance Improvement Demonstrated: ")
        
        return result
        
    except Exception as e:
        print(f" Error during analysis: {str(e)}")
        return None

async def demonstrate_different_queries():
    """Demonstrate the system with different types of queries"""
    
    ensemble = MultiPerspectiveEnsembleGraph()
    cot_enhancer = ChainOfThoughtEnhancer()
    
    queries = [
        {
            "name": "Climate Change Policy",
            "query": "How should governments balance economic growth with environmental protection in climate change policies?",
            "focus": "Policy and regulation"
        },
        {
            "name": "AI in Healthcare",
            "query": "What are the benefits and risks of implementing AI-powered diagnostic systems in healthcare?",
            "focus": "Technology adoption"
        },
        {
            "name": "Sustainable Transportation",
            "query": "How can cities transition to sustainable transportation systems while maintaining economic viability?",
            "focus": "Urban planning"
        }
    ]
    
    print("\n MULTI-QUERY DEMONSTRATION")
    print("=" * 80)
    
    for i, query_info in enumerate(queries, 1):
        print(f"\n Query {i}: {query_info['name']}")
        print(f"Focus: {query_info['focus']}")
        print(f"Query: {query_info['query']}")
        
        start_time = time.time()
        
        result = await ensemble.process_multi_perspective_query(
            query=query_info['query'],
            universal_cot=cot_enhancer.get_universal_cot_guidance(),
            chain_of_thought_1=cot_enhancer.get_perspective_specific_guidance("economic"),
            chain_of_thought_2=cot_enhancer.get_perspective_specific_guidance("environmental"),
            chain_of_thought_3=cot_enhancer.get_perspective_specific_guidance("technological")
        )
        
        processing_time = time.time() - start_time
        
        # Quick summary
        if result and not result.get("error"):
            judge_eval = result.get("judge_evaluation", {})
            quality_scores = judge_eval.get("quality_scores", {})
            
            print(f"   Completed in {processing_time:.1f}s")
            if quality_scores:
                avg_score = sum(quality_scores.values()) / len(quality_scores)
                best_model = max(quality_scores, key=quality_scores.get)
                print(f"   Average Quality Score: {avg_score:.3f}")
                print(f"   Best Model: {best_model.upper()}")
            
            final_synthesis = judge_eval.get("final_synthesis", "")
            if final_synthesis:
                print(f"   Key Insight: {final_synthesis[:150]}...")
        else:
            print(f"   Error or incomplete analysis")
        
        print("-" * 40)

async def main():
    """Main demonstration function"""
    print(" Enhanced Multi-Perspective LLM Ensemble System")
    print(" With Judge Involvement at Every Stage")
    print(" Performance Logging and Comparison")
    print(" Enhanced Chain of Thought Reasoning")
    print("\n" + "=" * 80)
    
    # Main demonstration
    result = await demonstrate_enhanced_multi_perspective_analysis()
    
    if result:
        print("\n Would you like to see demonstrations with different queries?")
        print("  Uncomment the line below to run multiple query demonstrations:")
        print("  # await demonstrate_different_queries()")
        
        # Uncomment to run multiple queries:
        # await demonstrate_different_queries()

if __name__ == "__main__":
    asyncio.run(main())
