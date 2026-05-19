import httpx
import os
from typing import Optional, Dict
from app.application.ports.ml_port import MLPort

class MLRestAdapter(MLPort):
    """Adaptador REST para consumir ms-machine-learning (puerto 8000)"""
    
    def __init__(self):
        # Puerto 8000 para ms-machine-learning
        self.base_url = os.getenv("ML_SERVICE_URL", "http://localhost:8000")
    
    async def get_prediction(self, zone_code: str) -> Optional[Dict]:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/predictions/{zone_code}"
                )
                if response.status_code == 200:
                    data = response.json()
                    # Adaptar respuesta al formato que espera el dominio
                    prediction_data = data.get("data", {}).get("prediction", {})
                    return {
                        "potential_value": prediction_data.get("potential_value", 0),
                        "confidence_score": prediction_data.get("confidence_score", 0),
                        "business_label": prediction_data.get("business_label", "Sin clasificar"),
                        "color_code": prediction_data.get("color_code", "#6b7280")
                    }
                return None
        except Exception as e:
            print(f"Error fetching prediction for {zone_code}: {e}")
            return None