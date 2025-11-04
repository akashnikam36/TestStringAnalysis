from typing import Dict, Optional, List
from models import StringAnalysisResponse
import re

class StringAnalyzer:
    def __init__(self):
        self._analysis_methods = {
            'word_count': self._word_count,
            'char_count': self._char_count,
        }
    def get_available_analyses(self) -> Dict[str,str]:
         return {
            'word_count': 'Total number of words in the text',
            'char_count': 'Total number of characters including spaces',
        }
    def analyze(self, text:str, requested_analyses: Optional[List[str]]=None)-> StringAnalysisResponse:
        if requested_analyses is None:
            analyses_to_perform = list(self._analysis_methods.keys())
        else:
            analyses_to_perform = requested_analyses
        
        invalid_analysis  = [a for a in analyses_to_perform if a not in self._analysis_methods]
        if invalid_analysis:
            raise ValueError(
                f"Invalid analysis types requested: {', '.join(invalid_analysis)}. "
                f"Available analyses: {', '.join(self._analysis_methods.keys())}"
            )
        
        result={}
        for analysis_name in analyses_to_perform:
            analysis_method = self._analysis_methods[analysis_name]
            result[analysis_name] = analysis_method(text)

        return StringAnalysisResponse(
            input_text = text,
            analyses = result
        )
    
    def _get_words(self, text: str)-> List[str]:
        words = re.findall(r'\b\w+\b', text)
        return [w for w in words if w]
    
    def _word_count(self,text:str) -> int:
        words = self._get_words(text)
        return len(words)
    
    def _char_count(self,text:str)-> int:
        return len(text)