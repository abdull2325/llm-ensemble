from typing import Dict, Any, List
from langchain_anthropic import ChatAnthropic
from config.settings import settings

class UnbiasedJudge:
    """Unbiased judge for evaluating and synthesizing model responses"""
    
    def __init__(self):
        # Use Claude as the judge (could be made configurable)
        self.judge_client = ChatAnthropic(
            api_key=settings.ANTHROPIC_API_KEY,
            model=settings.CLAUDE_MODEL,
            temperature=0.3,  # Lower temperature for more consistent judging
            max_tokens=settings.MAX_TOKENS
        )
    
    async def evaluate_responses(self, query: str, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate multiple model responses and provide synthesis"""
        
        judge_prompt = self._create_judge_prompt(query, responses)
        
        try:
            response = await self.judge_client.ainvoke(judge_prompt)
            return self._parse_judge_response(response.content)
        except Exception as e:
            return {
                "analysis": f"Error in evaluation: {str(e)}",
                "synthesis": "Unable to synthesize due to error",
                "scores": {model: 0.0 for model in responses.keys()},
                "reasoning": "Judge evaluation failed"
            }
    
    def _create_judge_prompt(self, query: str, responses: Dict[str, Any]) -> str:
        """Create a comprehensive prompt for the judge"""
        
        prompt = f"""
        You are an expert AI judge tasked with evaluating multiple AI model responses to a query. 
        Your role is to be completely unbiased and objective in your analysis.
        
        QUERY: {query}
        
        MODEL RESPONSES:
        """
        
        for model_name, response_data in responses.items():
            if response_data and hasattr(response_data, 'content'):
                prompt += f"""
        
        {model_name.upper()} RESPONSE:
        Content: {response_data.content}
        Confidence: {response_data.confidence}
        Reasoning: {response_data.reasoning}
        """
        
        prompt += """
        
        Please evaluate each response based on the following criteria:
        1. Accuracy and correctness of information
        2. Completeness and thoroughness of the answer
        3. Clarity and coherence of explanation
        4. Logical reasoning and evidence provided
        5. Relevance to the specific query asked
        
        Provide your evaluation in the following format:
        
        ANALYSIS:
        [Detailed analysis of each model's response, highlighting strengths and weaknesses]
        
        SYNTHESIS:
        [A comprehensive final answer that combines the best aspects of all responses, 
         corrects any errors, and provides the most complete and accurate response possible]
        
        SCORES:
        CLAUDE_SCORE: [0.0-1.0]
        GPT_SCORE: [0.0-1.0] 
        GROK_SCORE: [0.0-1.0]
        
        REASONING:
        [Explanation of your scoring methodology and key factors that influenced your evaluation]
        
        Be thorough but concise. Focus on providing the most helpful and accurate final synthesis.
        """
        
        return prompt
    
    def _parse_judge_response(self, response_content: str) -> Dict[str, Any]:
        """Parse the judge's response into structured data"""
        
        try:
            analysis = self._extract_section(response_content, "ANALYSIS")
            synthesis = self._extract_section(response_content, "SYNTHESIS")
            reasoning = self._extract_section(response_content, "REASONING")
            
            scores = {
                "claude": self._extract_score(response_content, "CLAUDE_SCORE"),
                "gpt": self._extract_score(response_content, "GPT_SCORE"),
                "grok": self._extract_score(response_content, "GROK_SCORE")
            }
            
            return {
                "analysis": analysis,
                "synthesis": synthesis,
                "scores": scores,
                "reasoning": reasoning
            }
            
        except Exception as e:
            return {
                "analysis": f"Error parsing judge response: {str(e)}",
                "synthesis": response_content,  # Return raw content as fallback
                "scores": {"claude": 0.5, "gpt": 0.5, "grok": 0.5},
                "reasoning": "Failed to parse structured response"
            }
    
    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a specific section from the judge response"""
        try:
            lines = content.split('\n')
            section_content = []
            capturing = False
            
            for line in lines:
                if line.strip().startswith(f"{section_name}:"):
                    capturing = True
                    # Include content after the colon on the same line
                    after_colon = line.split(':', 1)[1].strip()
                    if after_colon:
                        section_content.append(after_colon)
                elif capturing and line.strip().startswith(('ANALYSIS:', 'SYNTHESIS:', 'SCORES:', 'REASONING:', 'CLAUDE_SCORE:', 'GPT_SCORE:', 'GROK_SCORE:')):
                    break
                elif capturing:
                    section_content.append(line)
            
            result = '\n'.join(section_content).strip()
            return result if result else content  # Return full content if section not found
            
        except Exception:
            return content
    
    def _extract_score(self, content: str, score_name: str) -> float:
        """Extract a numerical score from the response"""
        try:
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith(f"{score_name}:"):
                    score_str = line.split(':', 1)[1].strip()
                    # Handle various score formats
                    score_str = score_str.replace('[', '').replace(']', '').strip()
                    return max(0.0, min(1.0, float(score_str)))  # Clamp between 0 and 1
            return 0.5  # Default neutral score
        except (ValueError, IndexError):
            return 0.5
    
    async def compare_models(self, evaluation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare model performance across multiple evaluations"""
        
        if not evaluation_history:
            return {"error": "No evaluation history provided"}
        
        model_scores = {"claude": [], "gpt": [], "grok": []}
        
        # Collect all scores
        for evaluation in evaluation_history:
            scores = evaluation.get("confidence_scores", {})
            for model in model_scores:
                if model in scores:
                    model_scores[model].append(scores[model])
        
        # Calculate statistics
        stats = {}
        for model, scores in model_scores.items():
            if scores:
                stats[model] = {
                    "average_score": sum(scores) / len(scores),
                    "max_score": max(scores),
                    "min_score": min(scores),
                    "total_evaluations": len(scores)
                }
            else:
                stats[model] = {
                    "average_score": 0.0,
                    "max_score": 0.0,
                    "min_score": 0.0,
                    "total_evaluations": 0
                }
        
        # Determine best performer
        best_model = max(stats.keys(), key=lambda m: stats[m]["average_score"])
        
        return {
            "model_statistics": stats,
            "best_performing_model": best_model,
            "total_evaluations": len(evaluation_history),
            "summary": f"Based on {len(evaluation_history)} evaluations, {best_model} performs best with an average score of {stats[best_model]['average_score']:.3f}"
        }
