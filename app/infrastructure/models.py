from sqlalchemy import JSON, Column, Float, Integer, String

from app.infrastructure.database import Base, BaseModelStore


# ─── TABLA 1: Base de datos de Recomendaciones ───
class RecommendationModel(Base):
    __tablename__ = "zone_recommendations"

    zone_code = Column(String, primary_key=True, index=True)
    zone_name = Column(String)
    current_score = Column(Float)
    potential_value = Column(Float)
    business_label = Column(String)
    top_recommendations = Column(JSON) # Aquí guardamos el Top 3 (CA 4)

# ─── TABLA 2: Base de datos del Motor de Reglas (Model Store) ───
class KnowledgeRuleModel(BaseModelStore):
    __tablename__ = "knowledge_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    factor = Column(String, index=True)
    impact = Column(String, index=True)
    action_text = Column(String)