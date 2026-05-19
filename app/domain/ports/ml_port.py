from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class MLPort(ABC):
    @abstractmethod
    async def get_prediction_data(self, zone_code: str) -> Optional[Dict[str, Any]]:
        """Debe retornar el payload de ML que incluye 'potential_value', 'business_label' y los 'main_factors'."""
        pass