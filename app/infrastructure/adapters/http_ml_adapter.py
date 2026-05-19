import os
from typing import Any, Dict, Optional

import httpx

from app.domain.ports.ml_port import MLPort
from app.schemas.external_schemas import MLResponseValidator  # <-- Importamos el schema


class HttpMLAdapter(MLPort):
    def __init__(self):
        self.base_url = os.getenv("MS_ML_URL", "http://ms-ml:8000")

    async def get_prediction_data(self, zone_code: str) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.base_url}/api/v1/ml/predictions/{zone_code}")
                if response.status_code == 200:
                    raw_json = response.json()
                    
                    #  Pydantic valida que el otro microservicio no rompió el contrato
                    validated_data = MLResponseValidator(**raw_json)
                    
                    # Retornamos un diccionario puro para que el puerto del dominio no dependa de Pydantic
                    return validated_data.data.model_dump()
                return None
            except Exception as e:
                # Si Pydantic falla, lanzará un ValidationError que será capturado aquí
                print(f"🚨 Error de red o validación de contrato conectando a ms-ml: {e}")
                return None