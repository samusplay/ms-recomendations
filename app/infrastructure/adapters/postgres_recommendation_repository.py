from typing import Optional

from sqlalchemy.orm import Session

from app.domain.entities.recommendation import (
    ActionableRecommendation,
    ZoneRecommendation,
)
from app.domain.repository_ports import RecommendationRepositoryPort
from app.infrastructure.models import RecommendationModel


class PostgresRecommendationRepository(RecommendationRepositoryPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def save_recommendation(self, recommendation: ZoneRecommendation) -> None:
        recs_dict = [
            {"factor": r.factor, "impact": r.impact, "weight": r.weight, "action_text": r.action_text}
            for r in recommendation.top_recommendations
        ]
        
        db_obj = self.db.query(RecommendationModel).filter(RecommendationModel.zone_code == recommendation.zone_code).first()
        if not db_obj:
            db_obj = RecommendationModel(zone_code=recommendation.zone_code)
            self.db.add(db_obj)
            
        db_obj.zone_name = recommendation.zone_name
        db_obj.current_score = recommendation.current_score
        db_obj.potential_value = recommendation.potential_value
        db_obj.business_label = recommendation.business_label
        db_obj.top_recommendations = recs_dict
        
        self.db.commit()

    def get_recommendation(self, zone_code: str) -> Optional[ZoneRecommendation]:
        db_obj = self.db.query(RecommendationModel).filter(RecommendationModel.zone_code == zone_code).first()
        if not db_obj:
            return None
            
        top_recs = [ActionableRecommendation(**rec) for rec in db_obj.top_recommendations]
        return ZoneRecommendation(
            zone_code=db_obj.zone_code,
            zone_name=db_obj.zone_name,
            current_score=db_obj.current_score,
            potential_value=db_obj.potential_value,
            business_label=db_obj.business_label,
            top_recommendations=top_recs
        )