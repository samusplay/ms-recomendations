import logging
from typing import Optional
from app.application.ports.score_port import ScorePort
from app.application.ports.ml_port import MLPort
from app.domain.services.recommendation_engine import RecommendationEngine
from app.domain.entities.recommendation import Recommendation

logger = logging.getLogger(__name__)

class GetRecommendationUseCase:
    """
    Caso de uso: Obtener recomendación para una zona
    Principios: SRP, DIP (depende de abstracciones)
    """
    
    def __init__(self, score_port: ScorePort, ml_port: MLPort):
        self._score_port = score_port
        self._ml_port = ml_port
    
    async def execute(self, zone_code: str) -> Optional[Recommendation]:
        # 1. Obtener datos a través de los puertos (abstracciones)
        score_data = await self._score_port.get_score(zone_code)
        prediction_data = await self._ml_port.get_prediction(zone_code)
        
        # 2. Validar que ambos servicios respondieron
        if not score_data:
            logger.warning(f"Score no disponible para zona {zone_code}")
            return None
        
        if not prediction_data:
            logger.warning(f"Predicción no disponible para zona {zone_code}")
            return None
        
        # 3. Delegar la lógica de negocio al DOMINIO (puro)
        return RecommendationEngine.create_recommendation(
            zone_code=zone_code,
            score_value=score_data.get("value", 0),
            score_level=score_data.get("level", "desconocido"),
            prediction_data=prediction_data
        )