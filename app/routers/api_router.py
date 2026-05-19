import re
import uuid
from fastapi import APIRouter, HTTPException, Depends, status
from app.application.use_cases.get_recommendation_use_case import GetRecommendationUseCase
from app.infrastructure.adapters.score_rest_adapter import ScoreRestAdapter
from app.infrastructure.adapters.ml_rest_adapter import MLRestAdapter

router = APIRouter()

def get_use_case() -> GetRecommendationUseCase:
    """Dependency Injection - Principio DIP"""
    return GetRecommendationUseCase(ScoreRestAdapter(), MLRestAdapter())

@router.get("/recommendations/{zone_code}")
async def get_recommendation(
    zone_code: str,
    use_case: GetRecommendationUseCase = Depends(get_use_case)
):
    trace_id = str(uuid.uuid4())
    
    # Validación en la capa de entrada (Controller)
    if not re.match(r"^\d{5}$|^\d{11}$", zone_code):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_ZONE_CODE_FORMAT",
                    "message": f"Formato inválido: '{zone_code}'. Debe tener 5 u 11 dígitos numéricos."
                },
                "trace_id": trace_id
            }
        )
    
    # Ejecutar caso de uso
    recommendation = await use_case.execute(zone_code)
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "DATA_NOT_AVAILABLE",
                    "message": f"No se pudieron obtener datos para la zona '{zone_code}'. Verifique que los servicios ms-ml y ms-scoring estén corriendo."
                },
                "trace_id": trace_id
            }
        )
    
    # Respuesta exitosa
    return {
        "success": True,
        "data": {
            "zone_code": recommendation.zone_code,
            "zone_name": recommendation.zone_name,
            "score": {
                "value": recommendation.score.value,
                "level": recommendation.score.level
            },
            "prediction": {
                "potential_value": recommendation.prediction.potential_value,
                "confidence_score": recommendation.prediction.confidence_score,
                "business_label": recommendation.prediction.business_label,
                "color_code": recommendation.prediction.color_code
            },
            "strengths": recommendation.strengths,
            "risks": recommendation.risks,
            "opportunities": recommendation.opportunities,
            "final_recommendation": recommendation.final_recommendation,
            "summary": recommendation.summary
        },
        "error": None,
        "trace_id": trace_id
    }

@router.get("/health")
async def health():
    return {"status": "healthy", "service": "ms-recommendations"}

@router.get("/")
async def root():
    return {"service": "ms-recommendations", "status": "running", "architecture": "hexagonal"}