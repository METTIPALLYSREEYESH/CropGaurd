"""
Weather Data Integration
Fetches current weather context to enrich AI analysis.
"""
import requests
import os

def get_weather_context(lat, lon, api_key=None):
    """
    Fetch current weather context for a location.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        api_key (str): OpenWeatherMap API Key
        
    Returns:
        dict: Weather context {temp, humidity, rain_status, description, icon}
    """
    # DEMO FAILSAFE: If no API key, return plausible mock data for a hackathon demo
    if not api_key:
        return {
            "temp": 28.5,
            "humidity": 45,
            "rain_status": "No recent rain",
            "description": "Clear Sky (Demo Data - Add API Key)",
            "icon": "☀️"  
        }
        
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            main = data.get('main', {})
            weather = data.get('weather', [{}])[0]
            
            # Simple icon mapping
            desc = weather.get('main', '').lower()
            icon = "🌥️"
            if 'clear' in desc: icon = "☀️"
            elif 'rain' in desc: icon = "🌧️"
            elif 'cloud' in desc: icon = "☁️"
            elif 'storm' in desc: icon = "⛈️"
            
            rain_val = data.get('rain', {}).get('1h', 0)
            rain_status = "Light Rain" if rain_val > 0 else "No rain"
            if rain_val > 5: rain_status = "Heavy Rain"
            
            return {
                "temp": main.get('temp', 0),
                "humidity": main.get('humidity', 0),
                "rain_status": rain_status,
                "description": weather.get('description', 'Unknown').capitalize(),
                "icon": icon
            }
    except Exception as e:
        print(f"Weather Fetch Error: {e}")
        
    # Fallback if API fails
    return {
        "temp": "--",
        "humidity": "--",
        "rain_status": "Unknown",
        "description": "Weather data unavailable",
        "icon": "❓"
    }
