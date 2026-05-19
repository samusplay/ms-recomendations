from typing import List, Optional

from pydantic import BaseModel


# Esquema para cada recomendación priorizada (HU-22 CA 1 y CA 4)
class ActionableRecommendationSchema(BaseModel):
    factor: str
    impact: str
    weight: float
    action_text: str

# Esquema para el objeto 'data' (lo que recibe el frontend)
class ZoneRecommendationDataSchema(BaseModel):
    zone_code: str
    zone_name: str
    current_score: float
    potential_value: float
    business_label: str
    top_recommendations: List[ActionableRecommendationSchema]

# Esquema para la respuesta exitosa (el contrato final)
class RecommendationSuccessResponse(BaseModel):
    success: bool = True
    data: ZoneRecommendationDataSchema
    error: Optional[dict] = None
    trace_id: str