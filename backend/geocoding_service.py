import re

import requests


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "Weather Intelligence Platform/1.0"}


def resolve_location(location: str) -> dict:
    location = location.strip()
    coordinate_match = re.match(r"^([-+]?[0-9]*\.?[0-9]+),\s*([-+]?[0-9]*\.?[0-9]+)$", location)
    if coordinate_match:
        latitude = float(coordinate_match.group(1))
        longitude = float(coordinate_match.group(2))
        return {"latitude": latitude, "longitude": longitude}

    params = {
        "q": location,
        "format": "json",
        "limit": 1,
    }
    response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=10)
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError("Location not found")

    latitude = float(data[0]["lat"])
    longitude = float(data[0]["lon"])
    return {"latitude": latitude, "longitude": longitude}
