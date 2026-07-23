import json
from datetime import datetime

from sqlalchemy.orm import Session

import models
import schemas


def get_weather_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WeatherRequest).order_by(models.WeatherRequest.request_date.desc()).offset(skip).limit(limit).all()


def get_weather_request(db: Session, request_id: int):
    return db.query(models.WeatherRequest).filter(models.WeatherRequest.id == request_id).first()


def create_weather_request(db: Session, request: schemas.WeatherRequestCreate, coordinates: dict, weather: dict, forecast_json: str):
    record = models.WeatherRequest(
        location=request.location,
        latitude=coordinates["latitude"],
        longitude=coordinates["longitude"],
        request_date=datetime.utcnow(),
        start_date=request.start_date,
        end_date=request.end_date,
        temperature=weather["temperature"],
        humidity=weather["humidity"],
        wind_speed=weather["wind_speed"],
        weather_condition=weather["weather_condition"],
        forecast_data=forecast_json,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_weather_request(db: Session, request_id: int, update: schemas.WeatherRequestUpdate):
    record = get_weather_request(db=db, request_id=request_id)
    if not record:
        raise ValueError("Request not found")

    location_changed = False
    if update.location and update.location != record.location:
        record.location = update.location
        location_changed = True
    if update.start_date:
        record.start_date = update.start_date
    if update.end_date:
        record.end_date = update.end_date

    if location_changed:
        from geocoding_service import resolve_location
        from weather_service import get_weather_by_coords

        coordinates = resolve_location(record.location)
        weather = get_weather_by_coords(coordinates["latitude"], coordinates["longitude"])
        if weather:
            record.latitude = coordinates["latitude"]
            record.longitude = coordinates["longitude"]
            record.temperature = weather["temperature"]
            record.humidity = weather["humidity"]
            record.wind_speed = weather["wind_speed"]
            record.weather_condition = weather["weather_condition"]
            record.forecast_data = json.dumps(weather["forecast"])

    db.commit()
    db.refresh(record)
    return record


def delete_weather_request(db: Session, request_id: int):
    record = get_weather_request(db=db, request_id=request_id)
    if not record:
        return False
    db.delete(record)
    db.commit()
    return True