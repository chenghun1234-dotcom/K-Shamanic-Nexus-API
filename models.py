from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union

class Weakness(BaseModel):
    item: str
    method: str

class Entity(BaseModel):
    id: str
    entity_name: str
    category: str
    region: str
    danger_level: str
    trigger: str
    weakness: Weakness
    background_lore: str
    attributes: List[str]

class Ritual(BaseModel):
    id: str
    name: str
    purpose: str
    ingredients: List[str]
    steps: List[str]
    risk_level: str
    success_probability: str

class DivinationMatch(BaseModel):
    saju_element: str
    compatible_entity_type: str
    taboo_actions: List[str]
    protective_item: str
    fortune_impact: str

class ScenarioRequest(BaseModel):
    region: str
    atmospheric_vibe: str = "Rural Horror"
    time_setting: str = "Modern"
    focus_entity: Optional[str] = None

class ScenarioResponse(BaseModel):
    title: str
    plot_summary: str
    key_locations: List[str]
    taboos: List[str]
    climax_event: str
    json_structured_data: Dict
