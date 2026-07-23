from typing import Dict


def generate_recommendation(question: str, weather: Dict) -> str:
    temperature = weather.get("temperature")
    wind_speed = weather.get("wind_speed")
    precipitation = weather.get("precipitation_probability")
    condition = weather.get("weather_condition", "clear").lower()

    recommendations = []
    if temperature is not None:
        if temperature >= 35:
            recommendations.append("It is very hot. Stay hydrated and avoid outdoor activity at noon.")
        elif temperature >= 25:
            recommendations.append("The weather is warm. Light clothing is recommended.")
        elif temperature >= 15:
            recommendations.append("The temperature is mild. A light jacket may be useful.")
        elif temperature >= 5:
            recommendations.append("It is cool. Wear a jacket and consider layering.")
        else:
            recommendations.append("It is cold. Wear a warm coat, hat, and gloves.")

    if precipitation is not None and precipitation >= 40:
        recommendations.append("Carry an umbrella or raincoat because rain is likely.")

    if wind_speed is not None and wind_speed >= 15:
        recommendations.append("It is windy. A windbreaker is recommended.")

    if "storm" in condition or "thunder" in condition:
        recommendations.append("Severe weather is possible. Avoid outdoor plans if you can.")
    elif "snow" in condition:
        recommendations.append("Snow is expected. Wear warm boots and be cautious on the roads.")

    if not recommendations:
        recommendations.append("The weather is moderate. Check local conditions before heading out.")

    return " ".join(recommendations)
