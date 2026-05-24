from abc import ABC, abstractmethod

class IAuditClient(ABC):
    @abstractmethod
    async def send_recommendation_event(
        self,
        zone_code: str,
        trace_id: str,
        details: dict
    ) -> None:
        pass
