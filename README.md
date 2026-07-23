# Weather Intelligence Platform

A full stack weather application built for the AI Engineer Intern technical assessment.

## Features

- Search weather worldwide by city, postal code, landmark, or GPS coordinates
- Retrieve real-time weather data from Open-Meteo API
- Geocode locations using OpenStreetMap Nominatim
- Store weather requests and results in SQLite
- CRUD operations for saved weather requests
- Export saved weather data as JSON, CSV, and PDF
- Simple AI assistant gives clothing recommendations based on weather

## Architecture

- Backend: Python FastAPI, SQLAlchemy, Pydantic
- Frontend: React + Vite
- Database: SQLite (development), easy to migrate to PostgreSQL
- External APIs: Open-Meteo, OpenStreetMap Nominatim, and Google Maps location links

## Installation

### Backend

1. Create and activate a Python virtual environment
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

## API Endpoints

- `GET /weather/{location}` - fetch weather for a location
- `POST /requests` - save a weather request
- `GET /requests` - list saved requests
- `GET /requests/{id}` - retrieve a saved request
- `PUT /requests/{id}` - update a saved request
- `DELETE /requests/{id}` - delete a saved request
- `GET /export/json` - export saved records as JSON
- `GET /export/csv` - export saved records as CSV
- `GET /export/pdf` - export saved records as PDF
- `POST /assistant` - get AI weather recommendation

## Notes

- The frontend assumes backend API is available at `http://localhost:8000`.
- All weather data is fetched dynamically from public APIs.

## Future Improvements

- Add authentication and user-specific request history
- Add Google Maps or YouTube integrations
- Improve UI design and add animations
- Add request validation and detailed forecast graphs
