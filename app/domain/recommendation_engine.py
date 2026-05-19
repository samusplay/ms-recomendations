from typing import Any, Dict, List


class RecommendationEngine:
    """
    Motor de Generación de Recomendaciones Accionables (HU-22 CA 1 y CA 4).
    Lógica de negocio pura. Sin frameworks ni bases de datos.
    """

    @classmethod
    def generate_actionable_recommendations(cls, main_factors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Recibe los factores evaluados, los prepara y los ordena por su peso absoluto.
        """
        recommendations = []

        for factor_data in main_factors:
            factor_name = factor_data.get("factor")
            impact = factor_data.get("impact")
            weight = factor_data.get("weight", 0.0)

            recommendations.append({
                "factor": factor_name,
                "impact": impact,
                "weight": weight
            })

        # CA 4: Priorización por Nivel de Impacto
        # Ordenamos la lista de mayor a menor basándonos en el valor absoluto del peso (weight)
        recommendations.sort(key=lambda x: abs(x["weight"]), reverse=True)

        # Retornamos estrictamente el Top 3 para evitar sobrecarga cognitiva al usuario final
        return recommendations[:3]