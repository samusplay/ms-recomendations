import httpx
import os
from typing import Optional, Dict
from app.application.ports.score_port import ScorePort

class ScoreRestAdapter(ScorePort):
    """Adaptador REST para consumir ms-analytics-scoring"""
    
    def __init__(self):
        # Puerto 8001 para ms-analytics-scoring
        self.base_url = os.getenv("SCORING_SERVICE_URL", "http://localhost:8001")
    
    async def get_score(self, zone_code: str) -> Optional[Dict]:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/score/{zone_code}"
                )
                if response.status_code == 200:
                    data = response.json()
                    # Adaptar respuesta al formato que espera el dominio
                    score_data = data.get("data", {}).get("score", {})
                    return {
                        "value": score_data.get("value", 0),
                        "level": score_data.get("level", "desconocido")
                    }
                return None
        except Exception as e:
            print(f"Error fetching score for {zone_code}: {e}")
            return None