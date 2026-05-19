from abc import ABC, abstractmethod
from typing import Optional, Dict

class ScorePort(ABC):
    """Puerto para obtener score desde ms-analytics-scoring"""
    
    @abstractmethod
    async def get_score(self, zone_code: str) -> Optional[Dict]:
        """Retorna: {'value': float, 'level': str}"""
        pass