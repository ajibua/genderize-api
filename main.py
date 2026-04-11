from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime, timezone

app = FastAPI()

# CORS configuration to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

GENDERIZE_URL = "https://api.genderize.io/"


@app.get("/api/classify")
async def classify_name(name: str = Query(...)):
    
    # Validate name parameter - must not be empty or whitespace
    if not name or not name.strip():
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Missing or empty name parameter"},
        )

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(GENDERIZE_URL, params={"name": name.strip()})

        # when unable to get valid response from upstream
        if response.status_code != 200:
            return JSONResponse(
                status_code=502,
                content={"status": "error", "message": "Upstream API returned an error"},
            )

        api_data = response.json()

        # when unable to detect gender or unable to get gender
        if api_data.get("gender") is None or api_data.get("count") == 0:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "error",
                    "message": "No prediction available for the provided name",
                },
            )

        gender      = api_data["gender"]
        probability = api_data["probability"]
        sample_size = api_data["count"]
        is_confident = probability >= 0.7 and sample_size >= 100
        processed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": {
                    "name": api_data["name"],
                    "gender": gender,
                    "probability": probability,
                    "sample_size": sample_size,
                    "is_confident": is_confident,
                    "processed_at": processed_at,
                },
            },
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=502,
            content={"status": "error", "message": "Failed to reach upstream API"},
        )

    except Exception:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Internal server error"},
        )