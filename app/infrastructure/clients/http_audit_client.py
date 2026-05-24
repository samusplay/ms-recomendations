import logging
import os
import httpx

from app.domain.ports.audit_client_interface import IAuditClient

logger = logging.getLogger(__name__)

class HttpAuditClient(IAuditClient):
    def __init__(self):
        self.base_url = os.getenv("MS_AUDIT_URL", "http://ms-auditoria:8000")

    async def send_recommendation_event(
        self,
        zone_code: str,
        trace_id: str,
        details: dict
    ) -> None:
        payload = {
            "event_type": "RECOMMENDATION_CREATED",
            "source_service": "ms-recommendations",
            "reference_id": zone_code,
            "trace_id": trace_id,
            "details": details,
            "status": "SUCCESS"
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/events",
                    json=payload,
                    timeout=3.0
                )
                response.raise_for_status()
        except Exception as e:
            logger.warning(f"Fallo persistencia evento auditoría recomendación zona {zone_code}: {e}")
