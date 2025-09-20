import os
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv


load_dotenv()

class WeatherAPI:
    """Client for OpenWeatherMap Current Weather API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the WeatherAPI client.

        Args:
            api_key: Your OpenWeatherMap API key. If None, will read from env 'Weather_api'.
        """
        self.api_key = api_key or os.getenv("Weather_api")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key not found. Set 'Weather_api' in your .env file.")

    def get_weather_by_city(
        self, city_name: str, country_code: Optional[str] = None, units: str = "metric"
    ) -> Optional[Dict[str, Any]]:
        """
        Get current weather data for a city.

        Args:
            city_name: Name of the city.
            country_code: Optional 2-letter country code (e.g., 'US', 'UK').
            units: 'metric' (Celsius), 'imperial' (Fahrenheit), or 'standard' (Kelvin).

        Returns:
            Dictionary with structured weather data, or None if error.
        """
        # Build query parameter
        query = f"{city_name},{country_code}" if country_code else city_name

        params = {
            "q": query,
            "appid": self.api_key,
            "units": units
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Structure the output for workflow use
            weather_info = {
                "city": data.get("name"),
                "country": data.get("sys", {}).get("country"),
                "description": data.get("weather", [{}])[0].get("description", "").capitalize(),
                "temperature": data.get("main", {}).get("temp"),
                "feels_like": data.get("main", {}).get("feels_like"),
                "humidity": data.get("main", {}).get("humidity"),
                "pressure": data.get("main", {}).get("pressure"),
                "wind_speed": data.get("wind", {}).get("speed"),
                "wind_deg": data.get("wind", {}).get("deg"),
                "visibility": data.get("visibility"),
            }
            return weather_info

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                return {"error": f"City '{city_name}' not found."}
            return {"error": f"HTTP error: {http_err}"}
        except Exception as e:
            return {"error": f"An error occurred: {e}"}

    @staticmethod
    def format_weather(weather_data: Dict[str, Any]) -> str:
        """
        Format weather information for display.

        Args:
            weather_data: Structured weather data dictionary.

        Returns:
            Formatted string for display.
        """
        if not weather_data or "error" in weather_data:
            return weather_data.get("error", "No weather data available.")

        lines = [
            f"🌤️  Weather in {weather_data.get('city', 'Unknown')}, {weather_data.get('country', '')}",
            "=" * 40,
            f"Description: {weather_data.get('description', 'N/A')}",
            f"Temperature: {weather_data.get('temperature', 'N/A')}°C",
            f"Feels like: {weather_data.get('feels_like', 'N/A')}°C",
            f"Humidity: {weather_data.get('humidity', 'N/A')}%",
            f"Pressure: {weather_data.get('pressure', 'N/A')} hPa",
            f"Wind Speed: {weather_data.get('wind_speed', 'N/A')} m/s",
            f"Wind Direction: {weather_data.get('wind_deg', 'N/A')}°",
            f"Visibility: {weather_data.get('visibility', 'N/A')} meters"
        ]
        return "\n".join(lines)
