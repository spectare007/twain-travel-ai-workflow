from app.weather import WeatherAPI

def get_weather_by_city(location: str) -> str:
    """
    Fetch and format the current weather for a given location using the WeatherAPI class.
    Returns a formatted string with weather information or an error message.
    """
    weather_api = WeatherAPI()
    weather_data = weather_api.get_weather_by_city(location)
    return WeatherAPI.format_weather(weather_data)
