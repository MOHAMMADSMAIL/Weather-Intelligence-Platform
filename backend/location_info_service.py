from typing import Dict


def get_location_info(display_name: str) -> Dict[str, str]:
    return {
        "description": display_name,
        "source": "OpenStreetMap Nominatim",
    }
