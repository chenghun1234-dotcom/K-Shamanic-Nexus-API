import json
from main import app
from fastapi.openapi.utils import get_openapi

def generate_spec():
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Customize for RapidAPI if needed
    openapi_schema["info"]["x-logo"] = {
        "url": "https://k-shamanic-nexus-api.vercel.app/static/logo.png"
    }

    with open("openapi.json", "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
    
    print("Successfully generated openapi.json")

if __name__ == "__main__":
    generate_spec()
