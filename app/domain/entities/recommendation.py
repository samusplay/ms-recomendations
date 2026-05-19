from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Score:
    value: float
    level: str

@dataclass
class Prediction:
    potential_value: float
    confidence_score: float
    business_label: str
    color_code: str

@dataclass
class Recommendation:
    zone_code: str
    zone_name: str
    score: Score
    prediction: Prediction
    strengths: List[str]
    risks: List[str]
    opportunities: List[str]
    final_recommendation: str
    summary: str