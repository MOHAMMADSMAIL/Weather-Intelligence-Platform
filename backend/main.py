from datetime import datetime
import io
import json
import os

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session

import crud
import export_service
import geocoding_service
import maps_service
import weather_service
from database import Base, SessionLocal, engine
import models
import schemas

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Weather Intelligence Platform API",
    description="Backend API for global weather search, history, export, and AI assistant.",
    version="1.0.0",
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def build_weather_response(location: str, latitude: float, longitude: float, weather: dict) -> dict:
    response = {
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        **weather,
    }
    map_data = maps_service.build_map_data(latitude, longitude)
    response.update(map_data)
    return response


@app.get("/weather/{location}", response_model=schemas.WeatherResponse)
def fetch_weather_by_location(location: str):
    try:
        coordinates = geocoding_service.resolve_location(location)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    weather = weather_service.get_weather_by_coords(coordinates["latitude"], coordinates["longitude"])
    if not weather:
        raise HTTPException(status_code=503, detail="Weather service unavailable")

    return build_weather_response(location, coordinates["latitude"], coordinates["longitude"], weather)


@app.get("/weather", response_model=schemas.WeatherResponse)
def fetch_weather(
    location: str | None = Query(None, description="City, postal code, landmark, or coordinates"),
    latitude: float | None = Query(None),
    longitude: float | None = Query(None),
):
    if latitude is not None and longitude is not None:
        weather = weather_service.get_weather_by_coords(latitude, longitude)
        if not weather:
            raise HTTPException(status_code=503, detail="Weather service unavailable")
        return build_weather_response(f"{latitude},{longitude}", latitude, longitude, weather)

    if not location:
        raise HTTPException(status_code=400, detail="Please provide a location or latitude and longitude")

    try:
        coordinates = geocoding_service.resolve_location(location)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    weather = weather_service.get_weather_by_coords(coordinates["latitude"], coordinates["longitude"])
    if not weather:
        raise HTTPException(status_code=503, detail="Weather service unavailable")

    return build_weather_response(location, coordinates["latitude"], coordinates["longitude"], weather)


@app.post("/requests", response_model=schemas.WeatherRequestOut)
def create_request(request: schemas.WeatherRequestCreate, db: Session = Depends(get_db)):
    if request.end_date < request.start_date:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")

    try:
        coordinates = geocoding_service.resolve_location(request.location)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    weather = weather_service.get_weather_by_coords(coordinates["latitude"], coordinates["longitude"])
    if not weather:
        raise HTTPException(status_code=503, detail="Weather service unavailable")

    forecast_json = json.dumps(weather["forecast"])
    record = crud.create_weather_request(db=db, request=request, coordinates=coordinates, weather=weather, forecast_json=forecast_json)
    return record


@app.get("/requests", response_model=list[schemas.WeatherRequestOut])
def list_requests(db: Session = Depends(get_db)):
    return crud.get_weather_requests(db=db)


@app.get("/requests/{request_id}", response_model=schemas.WeatherRequestOut)
def read_request(request_id: int, db: Session = Depends(get_db)):
    record = crud.get_weather_request(db=db, request_id=request_id)
    if not record:
        raise HTTPException(status_code=404, detail="Request not found")
    return record


@app.put("/requests/{request_id}", response_model=schemas.WeatherRequestOut)
def update_request(request_id: int, update: schemas.WeatherRequestUpdate, db: Session = Depends(get_db)):
    record = crud.get_weather_request(db=db, request_id=request_id)
    if not record:
        raise HTTPException(status_code=404, detail="Request not found")

    if update.end_date and update.start_date and update.end_date < update.start_date:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")

    try:
        updated = crud.update_weather_request(db=db, request_id=request_id, update=update)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return updated


@app.delete("/requests/{request_id}")
def delete_request(request_id: int, db: Session = Depends(get_db)):
    success = crud.delete_weather_request(db=db, request_id=request_id)
    if not success:
        raise HTTPException(status_code=404, detail="Request not found")
    return JSONResponse(content={"detail": "Record deleted"})


@app.get("/export/json")
def export_json(db: Session = Depends(get_db)):
    records = crud.get_weather_requests(db=db)
    return JSONResponse(content=[schemas.WeatherRequestOut.from_orm(record).dict() for record in records])


@app.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    records = crud.get_weather_requests(db=db)
    csv_bytes = export_service.build_csv(records)
    return StreamingResponse(io.BytesIO(csv_bytes), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=weather_requests.csv"})


@app.get("/export/pdf")
def export_pdf(db: Session = Depends(get_db)):
    records = crud.get_weather_requests(db=db)
    pdf_bytes = export_service.build_pdf(records)
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=weather_requests.pdf"})


@app.post("/assistant", response_model=schemas.AssistantResponse)
def assistant(request: schemas.AssistantRequest):
    weather = request.weather_data
    if not weather or not isinstance(weather, dict):
        raise HTTPException(status_code=400, detail="weather_data must be a JSON object")

    temperature = weather.get("temperature")
    wind_speed = weather.get("wind_speed")
    precipitation = weather.get("precipitation_probability")
    condition = weather.get("weather_condition", "clear")

    recommendation = ""
    if temperature is None:
        recommendation = "I need weather details to give a recommendation."
    else:
        if temperature <= 10:
            recommendation = "It is quite cold. A warm jacket and layers are recommended."
        elif temperature <= 18:
            recommendation = "A light jacket or sweater is a smart choice today."
        else:
            recommendation = "The weather is warm enough for light clothing."

        if precipitation and precipitation >= 40:
            recommendation += " Also bring a raincoat or umbrella because there is a good chance of rain."
        if wind_speed and wind_speed >= 15:
            recommendation += " Wind is strong, so consider a windbreaker."

    return {"recommendation": recommendation.strip()}