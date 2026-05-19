import os
from typing import Any, Dict, Optional

import httpx

from app.domain.ports.analytics_port import AnalyticsPort
from app.schemas.external_schemas import AnalyticsResponseValidator


class HttpAnalyticsAdapter(AnalyticsPort):
    def __init__(self):
        self.base_url = os.getenv("MS_ANALYTICS_URL", "http://ms-analytics:8000")

    async def get_zone_score(self, dataset_id: str, zone_code: str) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.base_url}/api/v1/analytics/zones/metrics/{dataset_id}")
                
                # 1. Verificamos que la petición fue exitosa
                if response.status_code != 200:
                    print(f"⚠️ ms-analytics retornó estado {response.status_code}")
                    return None
                
                raw_json = response.json()
                
                # 2. Validamos con Pydantic
                validated_response = AnalyticsResponseValidator(**raw_json)
                
                # 3. FILTRADO: Buscamos la zona exacta en la lista (evitamos retornar siempre el [0])
                if validated_response.data:
                    # Usamos next() para buscar el primero que coincida con el zone_code
                    match = next(
                        (zone for zone in validated_response.data if str(zone.zone_code) == str(zone_code)), 
                        None
                    )
                    
                    if match:
                        return match.model_dump()
                
                print(f"ℹ️ Zona {zone_code} no encontrada en el dataset {dataset_id}")
                return None

            except Exception as e:
                print(f"🚨 Error de red o validación de contrato conectando a ms-analytics: {e}")
                return None