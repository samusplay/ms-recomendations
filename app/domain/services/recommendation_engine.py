from typing import List, Dict, Any
from app.domain.entities.recommendation import Score, Prediction, Recommendation

class RecommendationEngine:
    """Motor de recomendaciones - Lógica de negocio pura, sin dependencias externas"""
    
    ZONES_NAMES = {
        "11001": "Bogotá",
        "05001": "Medellín", 
        "76001": "Cali",
        "08001": "Barranquilla",
        "54001": "Cúcuta",
        "73001": "Ibagué",
        "68001": "Bucaramanga",
    }
    
    @classmethod
    def create_recommendation(cls, zone_code: str, score_value: float,
                               score_level: str, prediction_data: Dict[str, Any]) -> Recommendation:
        """Método principal - Combina score y predicción para generar recomendación"""
        
        zone_name = cls.ZONES_NAMES.get(zone_code, "Zona consultada")
        prediction_value = prediction_data.get("potential_value", 0)
        
        return Recommendation(
            zone_code=zone_code,
            zone_name=zone_name,
            score=Score(value=score_value, level=score_level),
            prediction=Prediction(
                potential_value=prediction_value,
                confidence_score=prediction_data.get("confidence_score", 0),
                business_label=prediction_data.get("business_label", "Sin clasificar"),
                color_code=prediction_data.get("color_code", "#6b7280")
            ),
            strengths=cls._generate_strengths(score_value, prediction_value),
            risks=cls._generate_risks(score_value, prediction_value),
            opportunities=cls._generate_opportunities(score_value, prediction_value),
            final_recommendation=cls._generate_final_recommendation(score_value, prediction_value),
            summary=cls._generate_summary(score_value, prediction_value, zone_name)
        )
    
    @staticmethod
    def _generate_strengths(score: float, prediction: float) -> List[str]:
        strengths = []
        if score >= 70:
            strengths.append("✅ Puntuación general muy alta, zona prioritaria")
        elif score >= 50:
            strengths.append("✅ Puntuación general favorable para inversión")
        
        if prediction >= 70:
            strengths.append("📈 Alto potencial de crecimiento proyectado")
        elif prediction >= 50:
            strengths.append("📈 Potencial de crecimiento positivo")
        
        if score >= 60 and prediction >= 60:
            strengths.append("🎯 Alta consistencia entre evaluación actual y proyección")
        
        return strengths[:3] if strengths else ["⚠️ Requiere análisis adicional"]
    
    @staticmethod
    def _generate_risks(score: float, prediction: float) -> List[str]:
        risks = []
        if score < 40:
            risks.append("⚠️ Puntuación general baja, alto riesgo de inversión")
        elif score < 60:
            risks.append("📊 Puntuación moderada, evaluar detalladamente")
        
        if prediction < 40:
            risks.append("📉 Proyección de crecimiento limitada")
        
        if score < 50 and prediction < 50:
            risks.append("🔴 Inconsistencia entre datos actuales y proyección")
        
        return risks[:3] if risks else ["🌟 Oportunidad con riesgo controlado"]
    
    @staticmethod
    def _generate_opportunities(score: float, prediction: float) -> List[str]:
        opportunities = []
        if score >= 60:
            opportunities.append("💼 Ideal para expansión de negocio existente")
        if prediction >= 70:
            opportunities.append("🚀 Potencial para negocio ancla en la zona")
        if score >= 50 and prediction >= 50:
            opportunities.append("🏪 Apertura de nuevo local con alta probabilidad")
        if score >= 70 and prediction >= 60:
            opportunities.append("⭐ Zona candidata para inversión prioritaria")
        
        return opportunities[:3] if opportunities else ["🔍 Considerar estudio de mercado adicional"]
    
    @staticmethod
    def _generate_final_recommendation(score: float, prediction: float) -> str:
        avg = (score + prediction) / 2
        if avg >= 75:
            return "INVERTIR PRIORITARIAMENTE - Excelente oportunidad. Proceder con inversión."
        if avg >= 60:
            return "INVERTIR - Buena oportunidad. Realizar plan de implementación."
        if avg >= 45:
            return "EVALUAR CON PRECAUCIÓN - Potencial moderado. Requiere análisis adicional."
        if avg >= 30:
            return "MONITOREAR - Bajo potencial actual. Esperar evolución del mercado."
        return "NO INVERTIR - Alto riesgo identificado. Considerar zonas alternativas."
    
    @staticmethod
    def _generate_summary(score: float, prediction: float, zone_name: str) -> str:
        avg = (score + prediction) / 2
        if avg >= 70:
            return f"{zone_name} presenta oportunidad excepcional de inversión con score {score:.1f}/100 y potencial proyectado {prediction:.1f}/100."
        if avg >= 50:
            return f"{zone_name} muestra condiciones favorables con evaluación {score:.1f}/100 y potencial {prediction:.1f}/100. Considerar para expansión comercial."
        if avg >= 30:
            return f"{zone_name} tiene potencial moderado (score: {score:.1f}, proyección: {prediction:.1f}). Se recomienda análisis complementario."
        return f"{zone_name} no cumple criterios mínimos (score: {score:.1f}, proyección: {prediction:.1f}). Evaluar otras zonas."