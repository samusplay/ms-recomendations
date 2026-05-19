from pydantic import BaseModel

# ─── 1. ESQUEMAS PARA VALIDAR LA RESPUESTA DE MS-ML ───

class MLPredictionDetail(BaseModel):
    potential_value: float
    confidence_score: float
    business_label: str
    color_code: str

class MLPredictionData(BaseModel):
    zone_code: str
    prediction: MLPredictionDetail
    model_reference: str

class MLResponseValidator(BaseModel):
    success: bool
    data: MLPredictionData
    # Ignoramos trace_id y error si no los necesitamos en el dominio

# ─── 2. ESQUEMAS PARA VALIDAR LA RESPUESTA DE MS-ANALYTICS ───

class AnalyticsMetricsData(BaseModel):
    zone_code: str
    zone_name: str
    poblacion: float
    ingresos: float
    competencia: float

class AnalyticsResponseValidator(BaseModel):
    success: bool
    data: list[AnalyticsMetricsData] # Viene como una lista de zonas