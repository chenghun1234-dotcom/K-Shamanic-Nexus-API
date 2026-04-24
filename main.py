import json
import random
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Optional
from models import Entity, Ritual, DivinationMatch, ScenarioResponse, ScenarioRequest

app = FastAPI(
    title="K-Shamanic Nexus API",
    description="A high-performance API for Korean folklore, shamanism, and occult data.",
    version="1.0.0"
)

# CORS configuration for RapidAPI and UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data helper
def load_json(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# Endpoints
@app.get("/entities", response_model=List[Entity])
async def get_entities(category: Optional[str] = None, danger_level: Optional[str] = None):
    entities = load_json("data/entities.json")
    if category:
        entities = [e for e in entities if e["category"] == category]
    if danger_level:
        entities = [e for e in entities if e["danger_level"] == danger_level]
    return entities

@app.get("/rituals", response_model=List[Ritual])
async def get_rituals(purpose: Optional[str] = None):
    rituals = load_json("data/rituals.json")
    if purpose:
        rituals = [r for r in rituals if purpose.lower() in r["purpose"].lower()]
    return rituals

@app.get("/divination-logic", response_model=DivinationMatch)
async def get_divination_matching(saju_element: str):
    # Simplified Saju matching logic
    mappings = {
        "Fire": {
            "saju_element": "Fire (Hwa)",
            "compatible_entity_type": "Water Spirits (Su-Gwi)",
            "taboo_actions": ["Whistling at night", "Pouring water on embers"],
            "protective_item": "Red Silk pouch with ginger",
            "fortune_impact": "High risk of collision with vengeful spirits near bodies of water."
        },
        "Water": {
            "saju_element": "Water (Su)",
            "compatible_entity_type": "Mountain Spirits (Sang-sin)",
            "taboo_actions": ["Entering deep forests after sunset", "Stepping on old tree roots"],
            "protective_item": "Iron nails wrapped in white paper",
            "fortune_impact": "Potential for spiritual possession during foggy mountain crossings."
        }
    }
    return mappings.get(saju_element, mappings["Fire"])

@app.post("/plot-generator", response_model=ScenarioResponse)
async def generate_scenario(req: ScenarioRequest):
    templates = load_json("data/scenarios.json")
    entity = req.focus_entity or random.choice(["Dokkaebi", "Gumiho", "Jangsanbum", "Cheonyeo Gwishin"])
    template = random.choice(templates)
    
    title = f"Occult Log: {req.region} - {template['template_name']}"
    summary = template["structure"].format(region=req.region, entity=entity)
    
    return ScenarioResponse(
        title=title,
        plot_summary=summary,
        key_locations=["Mountain Path", "Old Shrine", "Village Community Center"],
        taboos=["Never whistles after sunset", "Do not cross the red threshold"],
        climax_event="The villagers gather at the shrine as the fog thickness increases.",
        json_structured_data={"vibe": req.atmospheric_vibe, "focus": entity, "template_id": template["id"]}
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "K-Shamanic Nexus API"}

# Static files for documentation
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
