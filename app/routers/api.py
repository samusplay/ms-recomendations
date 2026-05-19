from fastapi import APIRouter, HTTPException, status
import re
import uuid

api_router = APIRouter()

@api_router.get("/{zone_code}")
async def get_recommendation(zone_code: str):
    trace_id = str(uuid.uuid4())
    
    # Validar formato de zone_code
    if not re.match(r"^\d{5}$|^\d{11}$", zone_code):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_ZONE_CODE_FORMAT",
                    "message": f"Formato inválido: '{zone_code}'. Debe tener 5 u 11 dígitos."
                },
                "trace_id": trace_id
            }
        )
    
    # Respuesta mock mientras integramos
    zonas = {
        "11001": "Bogotá",
        "05001": "Medellín",
        "76001": "Cali",
        "08001": "Barranquilla",
        "54001": "Cúcuta"
    }
    
    return {
        "success": True,
        "data": {
            "zone_code": zone_code,
            "zone_name": zonas.get(zone_code, "Zona consultada"),
            "score": {"value": 75.5, "level": "alta oportunidad"},
            "prediction": {
                "potential_value": 80.2,
                "confidence_score": 0.85,
                "business_label": "Alto Potencial",
                "color_code": "#22c55e"
            },
            "strengths": ["✅ Puntuación general alta", "📈 Alto potencial de crecimiento"],
            "risks": ["📊 Evaluar competencia local"],
            "opportunities": ["💼 Ideal para expansión comercial"],
            "final_recommendation": "INVERTIR - Buena oportunidad",
            "summary": "La zona presenta condiciones favorables para inversión."
        },
        "error": None,
        "trace_id": trace_id
    }

@api_router.get("/health")
async def health():
    return {"status": "healthy", "service": "ms-recommendations"}

@api_router.get("/")
async def root():
    return {"service": "ms-recommendations", "status": "running"}
