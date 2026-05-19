from abc import ABC, abstractmethod
from typing import Optional, Dict

class MLPort(ABC):
    """Puerto para obtener predicción desde ms-machine-learning"""
    
    @abstractmethod
    async def get_prediction(self, zone_code: str) -> Optional[Dict]:
        """Retorna: {'potential_value': float, 'business_label': str, ...}"""
        pass