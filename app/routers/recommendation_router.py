import re
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importamos el orquestador (Aplicación)
from app.application.get_recommendation_use_case import GetRecommendationUseCase
from app.infrastructure.adapters.http_analytics_adapter import HttpAnalyticsAdapter

# Importamos los adaptadores (Infraestructura)
from app.infrastructure.adapters.http_ml_adapter import HttpMLAdapter
from app.infrastructure.adapters.postgres_knowledge_repository import (
    PostgresKnowledgeRepository,
)
from app.infrastructure.adapters.postgres_recommendation_repository import (
    PostgresRecommendationRepository,
)

# Importamos las dependencias de base de datos
from app.infrastructure.database import get_db, get_model_store_db

# Importamos el esquema de salida (Pydantic)
from app.schemas.recommendation_schema import RecommendationSuccessResponse

router = APIRouter()

def get_use_case(
    db: Session = Depends(get_db),
    model_db: Session = Depends(get_model_store_db)
) -> GetRecommendationUseCase:
    """
    Inyección de dependencias centralizada.
    Aquí instanciamos el Caso de Uso pasándole las implementaciones reales.
    """
    return GetRecommendationUseCase(
        ml_port=HttpMLAdapter(),
        analytics_port=HttpAnalyticsAdapter(),
        recommendation_repo=PostgresRecommendationRepository(db),
        knowledge_repo=PostgresKnowledgeRepository(model_db)
    )

# Usamos response_model para que Pydantic parsee la entidad del dominio a JSON automáticamente
@router.get("/{dataset_id}/{zone_code}", response_model=RecommendationSuccessResponse)
async def get_zone_recommendation(
    dataset_id:str,
    zone_code: str,
    use_case: GetRecommendationUseCase = Depends(get_use_case)
):
    trace_id = str(uuid.uuid4())
    
    # 1. Validación estructural (CA 1)
    if not re.match(r"^\d{1,11}$", zone_code):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "success": False,
                "data": None,
                "error": {"code": "INVALID_ZONE_CODE_FORMAT", "message": "Formato inválido."},
                "trace_id": trace_id
            }
        )
        
    # 2. Ejecutar el caso de uso
    recommendation = await use_case.execute(dataset_id, zone_code)
    
    # 3. Interrupción controlada
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {"code": "NOT_FOUND", "message": "Datos no disponibles."},
                "trace_id": trace_id
            }
        )
        
    # 4. Respuesta exitosa
    # Al usar 'response_model', Pydantic toma este diccionario y lo valida contra el esquema
    return {
        "success": True,
        "data": {
            "zone_code": recommendation.zone_code,
            "zone_name": recommendation.zone_name,
            "current_score": recommendation.current_score,
            "potential_value": recommendation.potential_value,
            "business_label": recommendation.business_label,
            "top_recommendations": [
                {
                    "factor": r.factor,
                    "impact": r.impact,
                    "weight": r.weight,
                    "action_text": r.action_text
                } for r in recommendation.top_recommendations
            ]
        },
        "error": None,
        "trace_id": trace_id
    }