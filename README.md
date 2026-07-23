
# Weather Intelligence Platform 🌦️

A full-stack weather application built for the **AI Engineer Intern Technical Assessment**.

Developed by:

**Mohammad Ismail**  
Artificial Intelligence & Data Science Student  
Al-Zarqa Private University, Jordan

---

# About PM Accelerator

**Product Manager Accelerator (PMA)** is a US-based company and AI learning and development hub that provides practical training, mentorship, and real-world projects for future AI and product professionals.

PMA's mission is to empower the next generation of technology professionals through hands-on experience, industry mentorship, and practical projects that help students develop the skills required for AI, product, and engineering careers.

LinkedIn:
https://www.linkedin.com/company/product-manager-accelerator/

---

# Assessment Completed

This project completes both:

- ✅ Tech Assessment #1 - Frontend Engineer
- ✅ Tech Assessment #2 - Backend Engineer

The project was developed as a full-stack weather platform combining:

- Frontend development
- Backend REST API development
- Database management
- External API integration
- CRUD operations
- Data export functionality


# Project Overview

Weather Intelligence Platform is a full-stack weather application that allows users to search for real-time weather information worldwide.

Users can search using:

- City names
- Postal codes
- Landmarks
- GPS coordinates

The system validates user input, retrieves weather data from external APIs, stores weather requests in a database, allows users to manage saved records, and provides weather-based recommendations.


# Features

## Weather Search

- Search weather worldwide by city, postal code, landmark, or GPS coordinates.
- Retrieve real-time weather information.
- Display:

  - Current temperature
  - Humidity
  - Wind speed
  - Weather condition
  - Precipitation probability
  - Five-day forecast


## Location Services

- Convert location names into coordinates using OpenStreetMap Nominatim API.
- Support GPS-based weather searching.


## Database Management

The application uses SQLite for data persistence.

Implemented CRUD operations:

- Create weather requests
- Read saved weather requests
- Update weather records
- Delete weather records


## Data Export

Users can export stored weather data into:

- JSON
- CSV
- PDF


## Weather Assistant

A simple AI-style assistant provides weather recommendations.

The assistant analyzes weather conditions and gives suggestions such as clothing recommendations.


# Architecture

```

Frontend (React + Vite)
    |
    |
  Axios

    |
    |
Backend (FastAPI)
    |
    |
Database (SQLite)
```
    |
    |
```
External APIs
(Open-Meteo + OpenStreetMap)

```


# Technology Stack


## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite


## Frontend

- React
- Vite
- JavaScript
- Axios
- React Router


## External APIs

### Open-Meteo API

Used for:

- Current weather information
- Temperature
- Humidity
- Wind speed
- Five-day forecast


### OpenStreetMap Nominatim API

Used for:

- Location searching
- Geocoding
- Converting location names into coordinates


### Google Maps

Used for:

- Generating location map links


# Project Structure

```

Weather-Intelligence-Platform

│
├── backend
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   │
│   ├── services
│   │   ├── weather_service.py
│   │   ├── geocoding_service.py
│   │   ├── export_service.py
│   │   ├── assistant_service.py
│   │   └── maps_service.py
│   │
│   ├── tests
│   │   └── test_api.py
│   │
│   └── requirements.txt
│
├── frontend
│   ├── src
│   │   ├── pages
│   │   │   ├── HomePage.jsx
│   │   │   ├── HistoryPage.jsx
│   │   │   ├── ExportPage.jsx
│   │   │   └── AssistantPage.jsx
│   │   │
│   │   ├── services
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── docs
├── README.md
└── .env.example

````


# UML Class Diagram

```mermaid
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
````

# Backend Responsibilities

## main.py

The main FastAPI entry point.

Responsible for:

* Creating API endpoints
* Handling HTTP requests
* Connecting services
* Returning responses

## database.py

Responsible for database configuration.

Contains:

* SQLAlchemy engine
* Database session
* Base configuration

## models.py

Defines database tables.

Main model:

`WeatherRequest`

Stores:

* Location
* Coordinates
* Weather information
* Forecast data
* Request dates

## schemas.py

Handles data validation using Pydantic.

Responsible for:

* Request validation
* Response formatting
* Data structure checking

## crud.py

Contains database operations:

* Create
* Read
* Update
* Delete

## weather_service.py

Handles Open-Meteo API communication.

Responsible for:

* Fetching weather data
* Processing forecast
* Formatting API response

## geocoding_service.py

Handles location conversion.

Responsible for:

* Receiving location input
* Returning latitude and longitude

## export_service.py

Creates exported files:

* JSON
* CSV
* PDF

## assistant_service.py

Provides weather recommendations based on weather conditions.

## maps_service.py

Creates map URLs for locations.

# Frontend Responsibilities

## App.jsx

Main application structure.

Responsible for:

* Routing
* Navigation

## main.jsx

Starts React application.

## api.js

Central API communication file.

Responsible for:

* Axios requests
* Backend communication

## HomePage.jsx

Main weather page.

Features:

* Search location
* GPS location
* Display weather
* Save requests

## HistoryPage.jsx

Shows saved weather history.

Features:

* Read data
* Update records
* Delete records

## ExportPage.jsx

Allows downloading:

* JSON
* CSV
* PDF

## AssistantPage.jsx

Displays weather recommendations.

# API Endpoints

| Method | Endpoint            | Description                  |
| ------ | ------------------- | ---------------------------- |
| GET    | /weather/{location} | Fetch weather                |
| GET    | /weather            | Fetch weather by coordinates |
| POST   | /requests           | Create request               |
| GET    | /requests           | Read requests                |
| GET    | /requests/{id}      | Read one request             |
| PUT    | /requests/{id}      | Update request               |
| DELETE | /requests/{id}      | Delete request               |
| GET    | /export/json        | Export JSON                  |
| GET    | /export/csv         | Export CSV                   |
| GET    | /export/pdf         | Export PDF                   |
| POST   | /assistant          | Weather recommendation       |

# Installation

## Backend

Create virtual environment:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Run:

```bash
uvicorn backend.main:app --reload --port 8000
```

## Frontend

Enter frontend folder:

```bash
cd frontend
```

Install packages:

```bash
npm install
```

Run:

```bash
npm run dev
```

# Notes

* Backend runs on:

```
http://localhost:8000
```

* All weather data is retrieved dynamically from APIs.
* No static weather information is used.
* SQLite can be migrated to PostgreSQL for production.

# Future Improvements

* Add authentication.
* Add user-specific history.
* Add weather alerts.
* Add advanced AI weather prediction.
* Improve UI animations.
* Add weather analytics dashboard.

```

```
