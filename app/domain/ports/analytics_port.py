from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class AnalyticsPort(ABC):
    @abstractmethod
    async def get_zone_score(self, zone_code: str) -> Optional[Dict[str, Any]]:
        """Debe retornar las métricas de la zona (el score base)."""
        pass