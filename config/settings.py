import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Configuration settings for the LLM Ensemble System"""
    
    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    XAI_API_KEY = os.getenv("XAI_API_KEY") or os.getenv("GROQ_API_KEY")  # Support both names
    
    # Model Configuration
    MAX_REFINEMENT_LOOPS = int(os.getenv("MAX_REFINEMENT_LOOPS", "3"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    
    # Model Names
    CLAUDE_MODEL = "claude-3-haiku-20240307"  # Using Haiku model which should be available
    GPT_MODEL = "gpt-4-turbo"  # Using stable GPT-4 model with standard parameters
    GROK_MODEL = "grok-2-1212"  # X.AI Grok model - trying different version
    
    # Validation
    @classmethod
    def validate_api_keys(cls):
        """Validate that all required API keys are present"""
        missing_keys = []
        
        if not cls.ANTHROPIC_API_KEY:
            missing_keys.append("ANTHROPIC_API_KEY")
        if not cls.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        if not cls.XAI_API_KEY:
            missing_keys.append("XAI_API_KEY or GROQ_API_KEY")
            
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
        
        return True

settings = Settings()
