from sqlalchemy.orm import Session

from app.domain.repository_ports import KnowledgeBaseRepositoryPort
from app.infrastructure.models import KnowledgeRuleModel


class PostgresKnowledgeRepository(KnowledgeBaseRepositoryPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_rule_text(self, factor: str, impact: str) -> str:
        #Debug que db estamos apuntando
        print(f"DEBUG: Repositorio consultando BD en: {self.db.bind.url}")
        rule = self.db.query(KnowledgeRuleModel).filter(
            KnowledgeRuleModel.factor == factor,
            KnowledgeRuleModel.impact == impact
        ).first()
        
        if rule:
            return rule.action_text
        return f"Evaluar detalladamente el factor '{factor}' por su impacto '{impact}'."