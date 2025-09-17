from abc import ABC, abstractmethod
from typing import Dict, Any
from langchain_anthropic import ChatAnthropic
from config.settings import settings

class BaseModel(ABC):
    """Abstract base class for all LLM models"""
    
    def __init__(self):
        self.model_name = ""
        self.client = None
        self._setup_client()
    
    @abstractmethod
    def _setup_client(self):
        """Setup the model client"""
        pass
    
    @abstractmethod
    async def generate_response(self, query: str, context: str = "") -> Dict[str, Any]:
        """Generate response to a query"""
        pass
    
    @abstractmethod
    async def refine_response(self, original_response: str, query: str, iteration: int) -> Dict[str, Any]:
        """Refine a previous response"""
        pass

class ClaudeModel(BaseModel):
    """Claude model implementation"""
    
    def _setup_client(self):
        """Setup Claude client"""
        self.model_name = settings.CLAUDE_MODEL
        self.client = ChatAnthropic(
            api_key=settings.ANTHROPIC_API_KEY,
            model=self.model_name,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS
        )
    
    async def generate_response(self, query: str, context: str = "") -> Dict[str, Any]:
        """Generate initial response using Claude"""
        prompt = f"""
        Context: {context}
        
        Query: {query}
        
        Please provide a comprehensive analysis of this query. Consider multiple perspectives and provide reasoning for your conclusions. Rate your confidence in your response on a scale of 0.0 to 1.0.
        
        Format your response as:
        ANALYSIS: [Your detailed analysis]
        REASONING: [Your reasoning process]
        CONFIDENCE: [0.0-1.0]
        """
        
        try:
            response = await self.client.ainvoke(prompt)
            content = response.content
            
            # Parse response components
            analysis = self._extract_section(content, "ANALYSIS")
            reasoning = self._extract_section(content, "REASONING")
            confidence = self._extract_confidence(content)
            
            return {
                "content": analysis,
                "reasoning": reasoning,
                "confidence": confidence,
                "raw_response": content
            }
        except Exception as e:
            return {
                "content": f"Error generating response: {str(e)}",
                "reasoning": "Error occurred during generation",
                "confidence": 0.0,
                "raw_response": ""
            }
    
    async def refine_response(self, original_response: str, query: str, iteration: int) -> Dict[str, Any]:
        """Refine Claude's previous response"""
        prompt = f"""
        Original Query: {query}
        
        Previous Response (Iteration {iteration-1}): {original_response}
        
        Please refine and improve the above response. Consider:
        1. Are there any gaps in reasoning?
        2. Could the analysis be more comprehensive?
        3. Are there alternative perspectives to consider?
        4. Can the explanation be clearer or more accurate?
        
        Provide your refined response and explain what improvements you made.
        
        Format your response as:
        REFINED_ANALYSIS: [Your improved analysis]
        IMPROVEMENTS: [What you improved and why]
        CONFIDENCE: [0.0-1.0]
        """
        
        try:
            response = await self.client.ainvoke(prompt)
            content = response.content
            
            refined_analysis = self._extract_section(content, "REFINED_ANALYSIS")
            improvements = self._extract_section(content, "IMPROVEMENTS")
            confidence = self._extract_confidence(content)
            
            return {
                "content": refined_analysis,
                "improvements": improvements,
                "confidence": confidence,
                "raw_response": content
            }
        except Exception as e:
            return {
                "content": original_response,
                "improvements": f"Error during refinement: {str(e)}",
                "confidence": 0.0,
                "raw_response": ""
            }
    
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
                elif capturing and line.strip().startswith(('REASONING:', 'CONFIDENCE:', 'REFINED_ANALYSIS:', 'IMPROVEMENTS:')):
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
                if line.strip().startswith('CONFIDENCE:'):
                    confidence_str = line.split(':', 1)[1].strip()
                    return float(confidence_str)
            return 0.7  # Default confidence
        except:
            return 0.7
