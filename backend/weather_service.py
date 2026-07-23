import requests

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_MAP = {
    0: "Clear",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Rain showers",
    81: "Heavy rain showers",
    82: "Violent rain showers",
    85: "Snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_weather_by_coords(latitude: float, longitude: float) -> dict | None:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": "relativehumidity_2m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode",
        "timezone": "auto",
    }
    response = requests.get(WEATHER_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    current = data.get("current_weather")
    daily = data.get("daily")
    hourly = data.get("hourly")
    if not current or not daily or not hourly:
        return None

    humidity = None
    current_time = current.get("time")
    if current_time and hourly.get("time") and hourly.get("relativehumidity_2m"):
        try:
            index = hourly["time"].index(current_time)
            humidity = hourly["relativehumidity_2m"][index]
        except ValueError:
            humidity = None

    forecast = []
    for index, day in enumerate(daily.get("time", [])):
        forecast.append({
            "date": day,
            "max_temp": daily.get("temperature_2m_max", [])[index],
            "min_temp": daily.get("temperature_2m_min", [])[index],
            "precipitation_probability": daily.get("precipitation_probability_max", [])[index],
            "condition": WEATHER_MAP.get(daily.get("weathercode", [])[index], "Unknown"),
        })

    weather_condition = WEATHER_MAP.get(current.get("weathercode", 0), "Clear")
    return {
        "temperature": current.get("temperature"),
        "humidity": humidity if humidity is not None else 0.0,
        "wind_speed": current.get("windspeed"),
        "weather_condition": weather_condition,
        "precipitation_probability": daily.get("precipitation_probability_max", [])[0] if daily.get("precipitation_probability_max") else None,
        "forecast": forecast[:5],
    }
