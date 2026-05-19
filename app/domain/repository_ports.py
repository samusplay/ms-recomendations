from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.recommendation import ZoneRecommendation


class KnowledgeBaseRepositoryPort(ABC):
    @abstractmethod
    def get_rule_text(self, factor: str, impact: str) -> str:
        """Busca en db_model_store el texto de acción para un factor e impacto específicos."""
        pass

class RecommendationRepositoryPort(ABC):
    @abstractmethod
    def save_recommendation(self, recommendation: ZoneRecommendation) -> None:
        """Guarda la recomendación generada en db_recommendations."""
        pass
    
    @abstractmethod
    def get_recommendation(self, zone_code: str) -> Optional[ZoneRecommendation]:
        """Obtiene una recomendación previamente calculada."""
        pass