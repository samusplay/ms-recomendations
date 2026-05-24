# app/application/get_recommendation_use_case.py
import asyncio
import logging
from typing import Any, Dict, List, Optional

from app.domain.entities.recommendation import (
    ActionableRecommendation,
    ZoneRecommendation,
)
from app.domain.ports.analytics_port import AnalyticsPort
from app.domain.ports.audit_client_interface import IAuditClient
from app.domain.ports.ml_port import MLPort
from app.domain.recommendation_engine import RecommendationEngine
from app.domain.repository_ports import (
    KnowledgeBaseRepositoryPort,
    RecommendationRepositoryPort,
)

logger = logging.getLogger(__name__)

class GetRecommendationUseCase:
    """
    Orquesta el flujo de la HU-22:
    1. Obtiene datos validados de ms-ml y ms-analytics.
    2. Convierte métricas a factores.
    3. Delega la priorización al motor de dominio.
    4. Consulta los textos de acción en la BD.
    5. Guarda el historial y retorna.
    """
    
    def __init__(
        self,
        ml_port: MLPort,
        analytics_port: AnalyticsPort,
        recommendation_repo: RecommendationRepositoryPort,
        knowledge_repo: KnowledgeBaseRepositoryPort,
        audit_client: IAuditClient
    ):
        self._ml_port = ml_port
        self._analytics_port = analytics_port
        self._recommendation_repo = recommendation_repo
        self._knowledge_repo = knowledge_repo
        self._audit_client = audit_client

    async def execute(self, dataset_id:str,zone_code: str, trace_id: str) -> Optional[ZoneRecommendation]:
        # 1. Obtener datos externos (ya pasaron por la Capa Anticorrupción de Pydantic)
        analytics_data = await self._analytics_port.get_zone_score(dataset_id, zone_code)
        #No le pasamos el datasetId
        ml_data = await self._ml_port.get_prediction_data(zone_code)
        # DEBUG: Identificar quién falla
        if not analytics_data:
            logger.error(f"❌ FALLO EN ms-analytics: No se obtuvieron datos para la zona {zone_code}")
        if not ml_data:
            logger.error(f"❌ FALLO EN ms-ml: No se obtuvieron datos para la zona {zone_code}")

        if not analytics_data or not ml_data:
            logger.warning(f"Datos incompletos para generar recomendación en la zona {zone_code}")
            return None

        # 2. Mapear las métricas crudas de Analytics a factores evaluables
        factors = self._map_metrics_to_factors(analytics_data)

        # 3. Delegar al Dominio la priorización (Cumple CA 4 de la HU-22)
        prioritized_factors = RecommendationEngine.generate_actionable_recommendations(factors)

        # 4. Construir las recomendaciones enriqueciéndolas con db_model_store
        top_recommendations = []
        for item in prioritized_factors:
            # El repositorio busca el texto exacto según el factor y su impacto
            action_text = self._knowledge_repo.get_rule_text(item["factor"], item["impact"])
            
            top_recommendations.append(
                ActionableRecommendation(
                    factor=item["factor"],
                    impact=item["impact"],
                    weight=item["weight"],
                    action_text=action_text
                )
            )

        # 5. Ensamblar la Entidad Pura del Dominio
        prediction_details = ml_data.get("prediction", {})
        recommendation = ZoneRecommendation(
            zone_code=zone_code,
            zone_name=analytics_data.get("zone_name", "Zona Desconocida"),
            current_score=analytics_data.get("ingresos", 0.0), # Ejemplo de score base
            potential_value=prediction_details.get("potential_value", 0.0),
            business_label=prediction_details.get("business_label", "Sin Clasificar"),
            top_recommendations=top_recommendations
        )

        # 6. Guardar el resultado en db_recommendations a través del puerto
        self._recommendation_repo.save_recommendation(recommendation)

        # 7. Notificación asíncrona a auditoría (degradación controlada)
        asyncio.create_task(self._notify_audit_async(recommendation, trace_id))

        return recommendation

    async def _notify_audit_async(self, recommendation: ZoneRecommendation, trace_id: str):
        fortalezas = []
        riesgos = []
        justificaciones = []

        for rec in recommendation.top_recommendations:
            if "Positivo" in rec.impact:
                fortalezas.append(f"{rec.factor} ({rec.impact})")
            elif "Penalización" in rec.impact:
                riesgos.append(f"{rec.factor} ({rec.impact})")
            justificaciones.append(rec.action_text)

        details = {
            "fortalezas": ", ".join(fortalezas) if fortalezas else "Ninguna",
            "riesgos": ", ".join(riesgos) if riesgos else "Ninguno",
            "justificaciones": " | ".join(justificaciones) if justificaciones else "Sin justificación"
        }

        await self._audit_client.send_recommendation_event(
            zone_code=recommendation.zone_code,
            trace_id=trace_id,
            details=details
        )

    def _map_metrics_to_factors(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Traduce los números crudos de Analytics en reglas de negocio"""
        factors = []
        
        poblacion = metrics.get("poblacion", 0.0)
        factors.append({
            "factor": "Población",
            "impact": "Positivo (Alto)" if poblacion > 0.5 else "Positivo (Medio)",
            "weight": poblacion
        })

        competencia = metrics.get("competencia", 0.0)
        factors.append({
            "factor": "Competencia",
            "impact": "Penalización Alta" if competencia > 0.5 else "Penalización Baja",
            "weight": competencia
        })

        ingresos = metrics.get("ingresos", 0.0)
        factors.append({
            "factor": "Ingresos",
            "impact": "Positivo (Alto)" if ingresos > 0.5 else "Positivo (Medio)",
            "weight": ingresos
        })

        return factors