#!/usr/bin/env python3
"""
Enhanced Chain of Thought module for the LLM Ensemble with Multi-Perspective Support
"""

from typing import Dict, Any, List

class ChainOfThoughtEnhancer:
    """Enhanced Chain of Thought reasoning for the ensemble with multi-perspective support"""
    
    def create_multi_perspective_cot_prompt(self, query: str, perspective: str, universal_guidance: str = "", specific_guidance: str = "") -> str:
        """Create a multi-perspective enhanced CoT prompt"""
        return f"""
        You are analyzing this query from the {perspective.upper()} perspective using enhanced chain-of-thought reasoning.
        
        QUERY: {query}
        PERSPECTIVE FOCUS: {perspective.upper()}
        
        {f"UNIVERSAL GUIDANCE: {universal_guidance}" if universal_guidance else ""}
        {f"{perspective.upper()} SPECIFIC GUIDANCE: {specific_guidance}" if specific_guidance else ""}
        
        Please apply the following multi-perspective reasoning chain:
        
        PERSPECTIVE_FRAME:
        - How does the {perspective} lens shape your approach to this question?
        - What aspects are most relevant from this {perspective} viewpoint?
        - What unique insights does this perspective offer?
        
        STEP_BY_STEP_ANALYSIS:
        1. PERSPECTIVE_UNDERSTANDING: [Interpret the query through {perspective} lens]
        2. DOMAIN_BREAKDOWN: [Break down into {perspective}-relevant components]
        3. PERSPECTIVE_REASONING: [Apply {perspective}-specific logic and frameworks]
        4. IMPLICATIONS: [What are the {perspective} implications and consequences?]
        5. PERSPECTIVE_SYNTHESIS: [Comprehensive {perspective} answer]
        
        PERSPECTIVE_LIMITATIONS:
        - What aspects might this {perspective} view miss?
        - How might other perspectives complement or challenge this view?
        - What are the inherent biases of this perspective?
        
        Please format your response as:
        PERSPECTIVE_FRAME: [Your {perspective} framing]
        PERSPECTIVE_UNDERSTANDING: [Your {perspective} interpretation]
        DOMAIN_BREAKDOWN: [Your {perspective} component analysis]
        PERSPECTIVE_REASONING: [Your {perspective} logic chain]
        IMPLICATIONS: [{perspective} implications]
        PERSPECTIVE_SYNTHESIS: [Your comprehensive {perspective} answer]
        PERSPECTIVE_LIMITATIONS: [Acknowledged limitations]
        CONFIDENCE: [0.0-1.0]
        """
    
    def create_perspective_comparison_cot_prompt(self, query: str, previous_analysis: str, previous_perspective: str, new_perspective: str, guidance: str = "") -> str:
        """Create CoT prompt for comparing and integrating multiple perspectives"""
        return f"""
        You are now integrating the {new_perspective.upper()} perspective with your previous {previous_perspective.upper()} analysis.
        
        ORIGINAL QUERY: {query}
        
        YOUR PREVIOUS {previous_perspective.upper()} ANALYSIS:
        {previous_analysis}
        
        {f"{new_perspective.upper()} GUIDANCE: {guidance}" if guidance else ""}
        
        Now apply enhanced reasoning to integrate perspectives:
        
        NEW_PERSPECTIVE_ANALYSIS:
        - Analyze the query from the {new_perspective} perspective
        - What new insights does this {new_perspective} view reveal?
        - How does {new_perspective} approach differ from {previous_perspective}?
        
        PERSPECTIVE_COMPARISON:
        - Where do {previous_perspective} and {new_perspective} perspectives align?
        - Where do they conflict or create tension?
        - Which perspective offers stronger insights for different aspects?
        
        INTEGRATION_REASONING:
        - How can these perspectives be synthesized?
        - What trade-offs or balances need to be considered?
        - What emerges from combining both viewpoints?
        
        ENHANCED_SYNTHESIS:
        - Provide a more comprehensive answer integrating both perspectives
        - Address conflicts and tensions explicitly
        - Identify areas where perspectives complement each other
        
        Format your response as:
        NEW_PERSPECTIVE_ANALYSIS: [Your {new_perspective} analysis]
        PERSPECTIVE_COMPARISON: [Comparison of {previous_perspective} vs {new_perspective}]
        INTEGRATION_REASONING: [How to combine the perspectives]
        ENHANCED_SYNTHESIS: [Your integrated multi-perspective answer]
        CONFIDENCE: [0.0-1.0]
        """
    
    def create_three_perspective_synthesis_cot_prompt(self, query: str, economic_analysis: str, environmental_analysis: str, tech_guidance: str = "") -> str:
        """Create CoT prompt for final three-perspective synthesis"""
        return f"""
        You are now performing the FINAL SYNTHESIS integrating ECONOMIC, ENVIRONMENTAL, and TECHNOLOGICAL perspectives.
        
        ORIGINAL QUERY: {query}
        
        YOUR PREVIOUS ANALYSES:
        ECONOMIC ANALYSIS: {economic_analysis}
        ENVIRONMENTAL ANALYSIS: {environmental_analysis}
        
        {f"TECHNOLOGICAL GUIDANCE: {tech_guidance}" if tech_guidance else ""}
        
        Apply comprehensive three-perspective reasoning:
        
        TECHNOLOGICAL_PERSPECTIVE:
        - Analyze the query from the technological perspective
        - What technological factors, innovations, or constraints are relevant?
        - How does technology shape or solve the challenges identified?
        
        THREE_WAY_COMPARISON:
        - Economic vs Environmental vs Technological priorities
        - Where do all three perspectives align?
        - What are the key tensions and trade-offs between them?
        
        HOLISTIC_REASONING:
        - How do economic, environmental, and technological factors interact?
        - What systemic relationships exist between these dimensions?
        - How can solutions address all three perspectives simultaneously?
        
        COMPREHENSIVE_SYNTHESIS:
        - Integrate insights from all three perspectives
        - Address major conflicts and propose balanced solutions
        - Provide a holistic answer that considers economic viability, environmental sustainability, and technological feasibility
        
        CONFIDENCE_ASSESSMENT:
        - Rate your confidence in this three-perspective synthesis
        - Identify areas of uncertainty or where additional perspectives might help
        - Explain your reasoning for the confidence level
        
        Format your response as:
        TECHNOLOGICAL_PERSPECTIVE: [Your technological analysis]
        THREE_WAY_COMPARISON: [Comparison across all three perspectives]
        HOLISTIC_REASONING: [Systems thinking across perspectives]
        COMPREHENSIVE_SYNTHESIS: [Final integrated answer]
        CONFIDENCE_ASSESSMENT: [Your confidence and reasoning]
        FINAL_CONFIDENCE: [0.0-1.0]
        """
    
    def create_cot_prompt(self, query: str, context: str = "") -> str:
        """Create an enhanced CoT prompt"""
        return f"""
        Context: {context}
        Query: {query}
        
        Please think through this step-by-step using the following reasoning chain:
        
        STEP 1 - UNDERSTANDING:
        - What is the core question being asked?
        - What are the key concepts involved?
        - What context is relevant?
        
        STEP 2 - ANALYSIS:
        - Break down the problem into components
        - Consider multiple perspectives
        - Identify potential complexities or edge cases
        
        STEP 3 - REASONING:
        - Apply logical reasoning to each component
        - Connect the pieces together
        - Consider cause-and-effect relationships
        
        STEP 4 - SYNTHESIS:
        - Combine insights from all steps
        - Form a comprehensive answer
        - Identify any remaining uncertainties
        
        STEP 5 - VALIDATION:
        - Double-check your reasoning
        - Consider alternative explanations
        - Rate your confidence and explain why
        
        Please format your response as:
        UNDERSTANDING: [Your interpretation of the question]
        ANALYSIS: [Your breakdown and multi-perspective analysis]
        REASONING: [Your step-by-step logical reasoning]
        SYNTHESIS: [Your comprehensive answer]
        VALIDATION: [Your self-check and confidence assessment]
        CONFIDENCE: [0.0-1.0]
        """
    
    def create_meta_cot_prompt(self, original_response: str, query: str) -> str:
        """Create a meta-reasoning prompt for refinement"""
        return f"""
        Original Query: {query}
        Previous Reasoning Chain: {original_response}
        
        Now, please perform META-REASONING on your previous response:
        
        META-STEP 1 - REASONING AUDIT:
        - Review each step of your previous reasoning
        - Identify any logical gaps or weak points
        - Check for biases or assumptions
        
        META-STEP 2 - ALTERNATIVE PATHS:
        - Consider alternative reasoning approaches
        - Explore different perspectives you might have missed
        - Think about contrarian viewpoints
        
        META-STEP 3 - EVIDENCE EVALUATION:
        - Assess the strength of your evidence
        - Identify what additional information would help
        - Consider uncertainty and limitations
        
        META-STEP 4 - REFINEMENT:
        - Improve weak areas in your reasoning
        - Strengthen your arguments where possible
        - Update your confidence based on this meta-analysis
        
        Format your response as:
        REASONING_AUDIT: [Your analysis of the previous reasoning]
        ALTERNATIVE_PATHS: [Other ways to approach this problem]
        EVIDENCE_EVALUATION: [Assessment of evidence quality]
        REFINED_REASONING: [Your improved reasoning chain]
        CONFIDENCE_DELTA: [How your confidence changed and why]
        """
    
    def extract_reasoning_chain(self, response: str) -> Dict[str, str]:
        """Extract the chain of thought components from a response"""
        components = {
            "understanding": "",
            "analysis": "",
            "reasoning": "",
            "synthesis": "",
            "validation": "",
            "perspective_frame": "",
            "perspective_understanding": "",
            "domain_breakdown": "",
            "perspective_reasoning": "",
            "implications": "",
            "perspective_synthesis": "",
            "perspective_limitations": "",
            "new_perspective_analysis": "",
            "perspective_comparison": "",
            "integration_reasoning": "",
            "enhanced_synthesis": "",
            "technological_perspective": "",
            "three_way_comparison": "",
            "holistic_reasoning": "",
            "comprehensive_synthesis": "",
            "confidence_assessment": ""
        }
        
        sections = ["UNDERSTANDING", "ANALYSIS", "REASONING", "SYNTHESIS", 
                   "VALIDATION", "PERSPECTIVE_FRAME", "PERSPECTIVE_UNDERSTANDING",
                   "DOMAIN_BREAKDOWN", "PERSPECTIVE_REASONING", "IMPLICATIONS",
                   "PERSPECTIVE_SYNTHESIS", "PERSPECTIVE_LIMITATIONS",
                   "NEW_PERSPECTIVE_ANALYSIS", "PERSPECTIVE_COMPARISON",
                   "INTEGRATION_REASONING", "ENHANCED_SYNTHESIS",
                   "TECHNOLOGICAL_PERSPECTIVE", "THREE_WAY_COMPARISON",
                   "HOLISTIC_REASONING", "COMPREHENSIVE_SYNTHESIS",
                   "CONFIDENCE_ASSESSMENT"]
        
        for section in sections:
            components[section.lower()] = self._extract_section(response, section)
        
        return components
    
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
                    ["UNDERSTANDING", "ANALYSIS", "REASONING", "SYNTHESIS", "VALIDATION", 
                     "CONFIDENCE", "PERSPECTIVE_FRAME", "PERSPECTIVE_UNDERSTANDING",
                     "DOMAIN_BREAKDOWN", "PERSPECTIVE_REASONING", "IMPLICATIONS",
                     "PERSPECTIVE_SYNTHESIS", "PERSPECTIVE_LIMITATIONS",
                     "NEW_PERSPECTIVE_ANALYSIS", "PERSPECTIVE_COMPARISON",
                     "INTEGRATION_REASONING", "ENHANCED_SYNTHESIS",
                     "TECHNOLOGICAL_PERSPECTIVE", "THREE_WAY_COMPARISON",
                     "HOLISTIC_REASONING", "COMPREHENSIVE_SYNTHESIS",
                     "CONFIDENCE_ASSESSMENT", "FINAL_CONFIDENCE"]):
                    break
                elif capturing:
                    section_content.append(line)
            
            return '\n'.join(section_content).strip()
        except:
            return ""
    
    def analyze_reasoning_quality(self, reasoning_chain: Dict[str, str]) -> Dict[str, Any]:
        """Analyze the quality of the reasoning chain"""
        quality_metrics = {
            "completeness": 0.0,
            "logical_consistency": 0.0,
            "depth": 0.0,
            "clarity": 0.0,
            "perspective_integration": 0.0
        }
        
        # Basic reasoning completeness
        basic_components = ["understanding", "analysis", "reasoning", "synthesis", "validation"]
        completed_basic = sum(1 for comp in basic_components if reasoning_chain.get(comp))
        quality_metrics["completeness"] = completed_basic / len(basic_components)
        
        # Perspective-specific completeness
        perspective_components = ["perspective_frame", "perspective_understanding", "perspective_reasoning", "perspective_synthesis"]
        completed_perspective = sum(1 for comp in perspective_components if reasoning_chain.get(comp))
        if completed_perspective > 0:
            quality_metrics["perspective_integration"] = completed_perspective / len(perspective_components)
        
        # Check for reasoning depth
        reasoning_text = reasoning_chain.get("reasoning", "") + reasoning_chain.get("perspective_reasoning", "")
        if len(reasoning_text) > 200:
            quality_metrics["depth"] = min(1.0, len(reasoning_text) / 500)
        
        # Check for logical connectors
        logical_words = ["because", "therefore", "thus", "consequently", "since", "given that", "however", "moreover"]
        connector_count = sum(1 for word in logical_words if word in reasoning_text.lower())
        quality_metrics["logical_consistency"] = min(1.0, connector_count / 3)
        
        # Overall clarity based on structure
        quality_metrics["clarity"] = (quality_metrics["completeness"] + quality_metrics["perspective_integration"]) / 2
        
        return quality_metrics
    
    def get_universal_cot_guidance(self) -> str:
        """Get standard universal CoT guidance for all perspectives"""
        return """
        UNIVERSAL REASONING PRINCIPLES:
        1. Break down complex issues into manageable components
        2. Consider both immediate and long-term implications
        3. Look for interconnections and system-level effects
        4. Acknowledge uncertainties and limitations in your analysis
        5. Consider multiple stakeholder viewpoints within your perspective
        6. Balance theoretical knowledge with practical constraints
        7. Be explicit about your assumptions and reasoning steps
        8. Consider unintended consequences and edge cases
        """
    
    def get_perspective_specific_guidance(self, perspective: str) -> str:
        """Get perspective-specific CoT guidance"""
        guidance = {
            "economic": """
            ECONOMIC PERSPECTIVE GUIDANCE:
            - Consider cost-benefit analysis and financial viability
            - Examine market dynamics, supply and demand factors
            - Analyze economic efficiency and resource allocation
            - Consider short-term costs vs long-term economic benefits
            - Examine impacts on different economic stakeholders
            - Consider macroeconomic and microeconomic effects
            - Analyze competitive advantages and market positioning
            """,
            "environmental": """
            ENVIRONMENTAL PERSPECTIVE GUIDANCE:
            - Assess environmental impact and sustainability
            - Consider resource consumption and waste generation
            - Examine ecosystem effects and biodiversity impacts
            - Analyze long-term environmental consequences
            - Consider circular economy principles
            - Examine climate change implications
            - Assess environmental justice and equity issues
            """,
            "technological": """
            TECHNOLOGICAL PERSPECTIVE GUIDANCE:
            - Analyze technical feasibility and implementation challenges
            - Consider scalability and infrastructure requirements
            - Examine innovation potential and technological advancement
            - Assess cybersecurity and safety implications
            - Consider user experience and adoption barriers
            - Analyze integration with existing technologies
            - Examine future technological trends and dependencies
            """
        }
        return guidance.get(perspective.lower(), "")

