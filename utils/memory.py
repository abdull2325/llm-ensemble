from typing import Dict, Any, List
import json
import os
from datetime import datetime
from dataclasses import dataclass

@dataclass
class EnsembleResult:
    """Structure for storing ensemble results"""
    query: str
    final_synthesis: str
    judge_analysis: str
    confidence_scores: Dict[str, float]
    model_responses: Dict[str, Any]
    processing_time: float
    total_iterations: int
    timestamp: str

class MemoryLogger:
    """Memory and logging system for the ensemble"""
    
    def __init__(self, log_file: str = "ensemble_memory.json"):
        self.log_file = log_file
        self.memory = self._load_memory()
    
    def _load_memory(self) -> List[Dict[str, Any]]:
        """Load existing memory from file"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def _save_memory(self):
        """Save memory to file"""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.memory, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def log_result(self, result: Dict[str, Any]):
        """Log an ensemble result"""
        ensemble_result = EnsembleResult(
            query=result.get("query", ""),
            final_synthesis=result.get("final_synthesis", ""),
            judge_analysis=result.get("judge_analysis", ""),
            confidence_scores=result.get("confidence_scores", {}),
            model_responses=result.get("model_responses", {}),
            processing_time=result.get("processing_time", 0.0),
            total_iterations=result.get("total_iterations", 0),
            timestamp=datetime.now().isoformat()
        )
        
        # Convert to dict and add to memory
        result_dict = {
            "query": ensemble_result.query,
            "final_synthesis": ensemble_result.final_synthesis,
            "judge_analysis": ensemble_result.judge_analysis,
            "confidence_scores": ensemble_result.confidence_scores,
            "model_responses": ensemble_result.model_responses,
            "processing_time": ensemble_result.processing_time,
            "total_iterations": ensemble_result.total_iterations,
            "timestamp": ensemble_result.timestamp
        }
        
        self.memory.append(result_dict)
        self._save_memory()
        
        print(f"📝 Logged result for query: {ensemble_result.query[:50]}...")
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        if not self.memory:
            return {"message": "No data available"}
        
        # Calculate averages
        total_entries = len(self.memory)
        avg_processing_time = sum(r["processing_time"] for r in self.memory) / total_entries
        avg_iterations = sum(r["total_iterations"] for r in self.memory) / total_entries
        
        # Calculate model confidence averages
        model_confidences = {"claude": [], "gpt": [], "grok": []}
        for result in self.memory:
            scores = result.get("confidence_scores", {})
            for model in model_confidences:
                if model in scores:
                    model_confidences[model].append(scores[model])
        
        avg_confidences = {}
        for model, scores in model_confidences.items():
            if scores:
                avg_confidences[model] = sum(scores) / len(scores)
            else:
                avg_confidences[model] = 0.0
        
        return {
            "total_queries_processed": total_entries,
            "average_processing_time": round(avg_processing_time, 2),
            "average_iterations": round(avg_iterations, 2),
            "average_model_confidences": avg_confidences,
            "latest_query": self.memory[-1]["query"] if self.memory else None,
            "latest_timestamp": self.memory[-1]["timestamp"] if self.memory else None
        }
    
    def search_memory(self, query_keyword: str) -> List[Dict[str, Any]]:
        """Search memory for queries containing a keyword"""
        results = []
        for result in self.memory:
            if query_keyword.lower() in result["query"].lower():
                results.append(result)
        return results
    
    def get_best_performing_model(self) -> Dict[str, Any]:
        """Determine which model performs best on average"""
        if not self.memory:
            return {"message": "No data available"}
        
        model_stats = {"claude": [], "gpt": [], "grok": []}
        
        for result in self.memory:
            scores = result.get("confidence_scores", {})
            for model in model_stats:
                if model in scores:
                    model_stats[model].append(scores[model])
        
        averages = {}
        for model, scores in model_stats.items():
            if scores:
                averages[model] = sum(scores) / len(scores)
            else:
                averages[model] = 0.0
        
        best_model = max(averages, key=averages.get) if averages else "unknown"
        
        return {
            "best_performing_model": best_model,
            "model_averages": averages,
            "total_evaluations": len(self.memory)
        }
    
    def clear_memory(self):
        """Clear all memory (use with caution)"""
        self.memory = []
        self._save_memory()
        print("🗑️ Memory cleared")
    
    def export_memory(self, filename: str = None) -> str:
        """Export memory to a file"""
        if filename is None:
            filename = f"ensemble_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.memory, f, indent=2, default=str)
            print(f"📤 Memory exported to {filename}")
            return filename
        except Exception as e:
            print(f"Error exporting memory: {e}")
            return ""
