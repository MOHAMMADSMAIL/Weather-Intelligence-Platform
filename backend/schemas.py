import json
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field, validator


class ForecastDay(BaseModel):
    date: str
    max_temp: float
    min_temp: float
    precipitation_probability: float
    condition: str


class WeatherResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    temperature: float
    humidity: float
    wind_speed: float
    weather_condition: str
    precipitation_probability: float | None = None
    forecast: list[ForecastDay]
    map_url: str | None = None
    map_provider: str | None = None


class WeatherRequestBase(BaseModel):
    location: str = Field(..., min_length=2)
    start_date: date
    end_date: date

    @validator("end_date")
    def validate_dates(cls, value, values):
        if "start_date" in values and value < values["start_date"]:
            raise ValueError("end_date must be after start_date")
        return value


class WeatherRequestCreate(WeatherRequestBase):
    pass


class WeatherRequestUpdate(BaseModel):
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None

    @validator("end_date")
    def validate_dates(cls, value, values):
        if "start_date" in values and values["start_date"] and value and value < values["start_date"]:
            raise ValueError("end_date must be after start_date")
        return value


class WeatherRequestOut(BaseModel):
    id: int
    location: str
    latitude: float
    longitude: float
    request_date: datetime
    start_date: date
    end_date: date
    temperature: float
    humidity: float
    wind_speed: float
    weather_condition: str
    forecast_data: list[dict[str, Any]]

    @validator("forecast_data", pre=True)
    def parse_forecast_data(cls, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception:
                return []
        return value

    class Config:
        orm_mode = True


class AssistantRequest(BaseModel):
    question: str = Field(..., min_length=5)
    weather_data: dict[str, Any]


class AssistantResponse(BaseModel):
    recommendation: str