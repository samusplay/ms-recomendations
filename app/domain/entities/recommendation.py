from dataclasses import dataclass
from typing import List


#Firma  de la base  de datos 
@dataclass
class ActionableRecommendation:
    factor: str
    impact: str
    weight: float
    action_text: str

@dataclass
class ZoneRecommendation:
    zone_code: str
    zone_name: str
    current_score: float
    potential_value: float
    business_label: str
    top_recommendations: List[ActionableRecommendation]