from app.infrastructure.database import SessionModelStore
from app.infrastructure.models import KnowledgeRuleModel


def seed_knowledge_base():
    db = SessionModelStore()
    try:
        db.query(KnowledgeRuleModel).delete()

        rules = [
            # ── POBLACIÓN ──────────────────────────────────────────────
            KnowledgeRuleModel(
                factor="Población",
                impact="Positivo (Alto)",
                action_text=(
                    "La zona concentra una alta densidad poblacional, lo que representa "
                    "un mercado potencial amplio. Se recomienda priorizar esta zona para "
                    "apertura de establecimiento, especialmente en sectores de consumo "
                    "masivo, servicios cotidianos o retail de alta rotación."
                ),
            ),
            KnowledgeRuleModel(
                factor="Población",
                impact="Positivo (Medio)",
                action_text=(
                    "La zona presenta una base poblacional moderada con margen de crecimiento. "
                    "Se recomienda validar la demanda con un modelo de operación liviano antes "
                    "de realizar una inversión fija significativa en el territorio."
                ),
            ),
            # ── COMPETENCIA ────────────────────────────────────────────
            KnowledgeRuleModel(
                factor="Competencia",
                impact="Penalización Alta",
                action_text=(
                    "La zona presenta alta saturación de competidores en el sector. "
                    "Se recomienda desarrollar una propuesta diferenciada por precio, "
                    "experiencia o segmento desatendido, o evaluar zonas aledañas con "
                    "menor concentración comercial para reducir el riesgo de entrada."
                ),
            ),
            KnowledgeRuleModel(
                factor="Competencia",
                impact="Penalización Baja",
                action_text=(
                    "La competencia en la zona es manejable. Se recomienda establecer "
                    "presencia temprana y construir fidelización con los clientes locales "
                    "para consolidar participación de mercado antes de que ingresen nuevos actores."
                ),
            ),
            # ── INGRESOS ───────────────────────────────────────────────
            KnowledgeRuleModel(
                factor="Ingresos",
                impact="Positivo (Alto)",
                action_text=(
                    "La zona registra un nivel de ingresos alto, indicando capacidad de "
                    "gasto favorable. Se recomienda orientar la oferta hacia productos o "
                    "servicios de mayor valor agregado, priorizando calidad y experiencia "
                    "sobre precio para maximizar el margen comercial."
                ),
            ),
            KnowledgeRuleModel(
                factor="Ingresos",
                impact="Positivo (Medio)",
                action_text=(
                    "Los ingresos de la zona son moderados y estables. Se recomienda "
                    "estructurar una propuesta accesible con opciones de pago flexibles, "
                    "enfocada en sectores de consumo frecuente que se adapten al poder "
                    "adquisitivo predominante del territorio."
                ),
            ),
        ]

        db.add_all(rules)
        db.commit()
        print(f"✅ {len(rules)} reglas insertadas exitosamente en knowledge_rules.")
    except Exception as e:
        db.rollback()
        print(f"🚨 Error al poblar la base de datos: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_knowledge_base()