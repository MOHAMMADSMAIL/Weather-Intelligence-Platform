from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Float, Integer, String, Text

from database import Base


class WeatherRequest(Base):
    __tablename__ = "weather_requests"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(255), index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    request_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    weather_condition = Column(String(128), nullable=False)
    forecast_data = Column(Text, nullable=False)