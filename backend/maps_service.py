from typing import Dict


def build_map_data(latitude: float, longitude: float) -> Dict[str, str]:
    return {
        "provider": "Google Maps",
        "map_url": f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}",
    }
