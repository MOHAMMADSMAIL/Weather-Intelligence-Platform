# Weather Intelligence Platform 🌦️

## About PM Accelerator

**Product Manager Accelerator (PMA)** is a US-based company and 
award-winning AI learning and development hub, featuring mentors 
from top-tier companies such as Google, Meta, Apple, and Nvidia.

PMA's mission is to empower the next generation of AI and product 
professionals through hands-on experience, mentorship, and 
real-world projects. Their AI PM Bootcamp helps students land 
product and engineering roles at FAANG companies and top tech 
startups. PMA also runs PMA Kids, a nonprofit offering free AI 
Bootcamp training to underserved communities worldwide.

🔗 LinkedIn: https://www.linkedin.com/company/product-manager-accelerator/

---

## Project Overview

A full stack weather application built by **Mohammad Mohsen Ismail 
Ismail** as part of the PM Accelerator AI Engineer Intern Technical 
Assessment.

The platform allows users to search for real-time weather data 
worldwide, save and manage weather requests, and export weather 
records in multiple formats.

---

## Features

- Search weather worldwide by city, postal code, landmark, or 
  GPS coordinates
- Retrieve real-time weather data from Open-Meteo API
- Geocode locations using OpenStreetMap Nominatim
- Store weather requests and results in SQLite
- Full CRUD operations for saved weather requests
- Export saved weather data as JSON, CSV, and PDF
- AI assistant that gives clothing recommendations based on weather

---

## Architecture

- **Backend:** Python FastAPI, SQLAlchemy, Pydantic
- **Frontend:** React + Vite
- **Database:** SQLite (development), easy to migrate to PostgreSQL
- **External APIs:** Open-Meteo, OpenStreetMap Nominatim, 
  Google Maps location links

---

## Project Structure
classDiagram
  class WeatherRequest {
    +int id
    +str location
    +float latitude
    +float longitude
    +datetime request_date
    +date start_date
    +date end_date
    +float temperature
    +float humidity
    +float wind_speed
    +str weather_condition
    +Text forecast_data
  }

  class ForecastDay {
    +str date
    +float max_temp
    +float min_temp
    +float precipitation_probability
    +str condition
  }

  class WeatherResponse {
    +str location
    +float latitude
    +float longitude
    +float temperature
    +float humidity
    +float wind_speed
    +str weather_condition
    +float precipitation_probability
    +list forecast
    +str map_url
    +str map_provider
  }

  class WeatherRequestCreate {
    +str location
    +date start_date
    +date end_date
  }

  class WeatherRequestUpdate {
    +str location
    +date start_date
    +date end_date
  }

  class WeatherRequestOut {
    +int id
    +str location
    +float latitude
    +float longitude
    +datetime request_date
    +date start_date
    +date end_date
    +float temperature
    +float humidity
    +float wind_speed
    +str weather_condition
    +list forecast_data
  }

  class AssistantRequest {
    +str question
    +dict weather_data
  }

  class AssistantResponse {
    +str recommendation
  }

  WeatherRequest <|-- WeatherRequestCreate
  WeatherRequest <|-- WeatherRequestUpdate
  WeatherRequest <|-- WeatherRequestOut
  WeatherResponse --> ForecastDay

---

## Installation and Running

### Backend

1. Create and activate a Python virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

3. Run backend server:
```bash
uvicorn backend.main:app --reload --port 8000
```

### Frontend

1. Change into the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the app:
```bash
npm run dev
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/weather/{location}` | Fetch real-time weather |
| POST | `/requests` | Save a weather request |
| GET | `/requests` | List all saved requests |
| GET | `/requests/{id}` | Get a specific request |
| PUT | `/requests/{id}` | Update a request |
| DELETE | `/requests/{id}` | Delete a request |
| GET | `/export/json` | Export as JSON |
| GET | `/export/csv` | Export as CSV |
| GET | `/export/pdf` | Export as PDF |
| POST | `/assistant` | Get AI weather recommendation |

---

## Author

**Mohammad Mohsen Ismail Ismail**
Artificial Intelligence & Data Science Student
Al-Zarqa Private University, Jordan
AWS Certified AI Practitioner (AIF-C01)

---

## Notes

- The frontend assumes backend API is available at 
  `http://localhost:8000`
- All weather data is fetched dynamically from public APIs
- No static data is used in this application

