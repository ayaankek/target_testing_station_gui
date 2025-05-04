import requests

def get_weather_data(latitude=38.5449, longitude=-121.7405):
    """
    Fetches current temperature (°C) and pressure (Psi) for Davis, CA using Open-Meteo API.

    Args:
        latitude (float): Latitude of the location. Default is Davis, CA.
        longitude (float): Longitude of the location. Default is Davis, CA.

    Returns:
        tuple: (temperature_celsius, pressure_psi)
    """
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}"
            f"&current=temperature_2m,pressure_msl"
        )
        response = requests.get(url)
        response.raise_for_status()

        data = response.json().get("current", {})
        temperature = data.get("temperature_2m")
        pressure_hpa = data.get("pressure_msl")

        if temperature is None or pressure_hpa is None:
            raise ValueError("Missing temperature or pressure in API response.")

        # Convert hPa to psi: 1 hPa = 0.0145038 psi
        pressure_psi = pressure_hpa * 0.0145038

        return temperature, pressure_psi

    except Exception as e:
        print("⚠ Failed to fetch weather data:", e)
        return 25, 14.7  # fallback temperature and pressure (°C, psi)
