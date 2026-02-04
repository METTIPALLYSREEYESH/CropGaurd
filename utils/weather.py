"""
Weather Data Fetching using Open-Meteo API
Free weather API - no API key required!
"""

import requests
from datetime import datetime, timedelta

def fetch_weather_data(latitude, longitude):
    """
    Fetch current weather data from Open-Meteo API
    
    Args:
        latitude (float): Latitude of the location
        longitude (float): Longitude of the location
        
    Returns:
        dict: Weather data with temperature, precipitation, wind speed, etc.
    """
    try:
        # Open-Meteo API endpoint (FREE - no API key needed!)
        url = "https://api.open-meteo.com/v1/forecast"
        
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m,weather_code',
            'daily': 'precipitation_sum',
            'timezone': 'auto',
            'forecast_days': 16  # Get last 15 days of precipitation data
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        current = data.get('current', {})
        daily = data.get('daily', {})
        
        # Calculate days since last rain
        days_since_rain = calculate_days_since_rain(daily.get('precipitation_sum', []))
        
        # Get weather description from code
        weather_code = current.get('weather_code', 0)
        weather_desc = get_weather_description(weather_code)
        
        return {
            'temperature': current.get('temperature_2m', 25),  # Celsius
            'precipitation': current.get('precipitation', 0),  # mm
            'wind_speed': current.get('wind_speed_10m', 0),  # km/h
            'humidity': current.get('relative_humidity_2m', 50),  # %
            'weather_code': weather_code,
            'weather_description': weather_desc,
            'days_since_rain': days_since_rain,
            'is_raining': current.get('precipitation', 0) > 0,
            'timestamp': current.get('time', datetime.now().isoformat())
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Weather API error: {e}")
        # Return default values if API fails
        return get_default_weather()
    except Exception as e:
        print(f"Weather processing error: {e}")
        return get_default_weather()

def calculate_days_since_rain(precipitation_data):
    """
    Calculate how many days since last significant rain
    
    Args:
        precipitation_data (list): List of daily precipitation values
        
    Returns:
        int: Number of days since last rain (>1mm)
    """
    if not precipitation_data:
        return 0
    
    # Reverse to check from most recent day backwards
    for i, precip in enumerate(reversed(precipitation_data)):
        if precip and precip > 1.0:  # Significant rain = >1mm
            return i
    
    return len(precipitation_data)  # No rain in entire period

def get_weather_description(weather_code):
    """
    Convert WMO weather code to description
    
    Args:
        weather_code (int): WMO weather code
        
    Returns:
        str: Weather description
    """
    # WMO Weather interpretation codes
    weather_codes = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Foggy',
        48: 'Depositing rime fog',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        61: 'Slight rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        71: 'Slight snow',
        73: 'Moderate snow',
        75: 'Heavy snow',
        77: 'Snow grains',
        80: 'Slight rain showers',
        81: 'Moderate rain showers',
        82: 'Violent rain showers',
        85: 'Slight snow showers',
        86: 'Heavy snow showers',
        95: 'Thunderstorm',
        96: 'Thunderstorm with slight hail',
        99: 'Thunderstorm with heavy hail'
    }
    
    return weather_codes.get(weather_code, 'Unknown')

def get_default_weather():
    """
    Return default weather data when API is unavailable
    
    Returns:
        dict: Default weather data
    """
    return {
        'temperature': 28,
        'precipitation': 0,
        'wind_speed': 10,
        'humidity': 60,
        'weather_code': 1,
        'weather_description': 'Partly cloudy',
        'days_since_rain': 7,
        'is_raining': False,
        'timestamp': datetime.now().isoformat()
    }

def get_farmer_weather_status(weather_data, lang='en'):
    """
    Convert weather data to farmer-friendly status
    
    Args:
        weather_data (dict): Weather data from fetch_weather_data
        lang (str): Language code
        
    Returns:
        dict: Farmer-friendly weather status
    """
    temp = weather_data['temperature']
    wind = weather_data['wind_speed']
    days_no_rain = weather_data['days_since_rain']
    is_raining = weather_data['is_raining']
    
    # Temperature status
    if temp > 35:
        temp_status = 'very_hot' if lang == 'en' else 'बहुत गर्म' if lang == 'hi' else 'చాలా వేడి'
        temp_icon = '🔥'
    elif temp > 30:
        temp_status = 'hot' if lang == 'en' else 'गर्म' if lang == 'hi' else 'వేడి'
        temp_icon = '☀️'
    elif temp > 20:
        temp_status = 'warm' if lang == 'en' else 'सामान्य' if lang == 'hi' else 'సాధారణం'
        temp_icon = '🌤️'
    else:
        temp_status = 'cool' if lang == 'en' else 'ठंडा' if lang == 'hi' else 'చల్లగా'
        temp_icon = '🌥️'
    
    # Rain status
    if is_raining:
        rain_status = 'raining_now' if lang == 'en' else 'बारिश हो रही है' if lang == 'hi' else 'వర్షం పడుతోంది'
        rain_icon = '🌧️'
    elif days_no_rain > 14:
        rain_status = 'no_rain_long' if lang == 'en' else 'बहुत दिनों से नहीं' if lang == 'hi' else 'చాలా రోజులుగా లేదు'
        rain_icon = '☀️'
    elif days_no_rain > 7:
        rain_status = 'no_rain_week' if lang == 'en' else 'हफ्ते से नहीं' if lang == 'hi' else 'వారం నుండి లేదు'
        rain_icon = '🌤️'
    else:
        rain_status = 'recent_rain' if lang == 'en' else 'हाल में हुई' if lang == 'hi' else 'ఇటీవల పడింది'
        rain_icon = '💧'
    
    # Wind status
    if wind > 30:
        wind_status = 'strong' if lang == 'en' else 'तेज' if lang == 'hi' else 'బలమైన'
        wind_icon = '💨💨'
    elif wind > 15:
        wind_status = 'moderate' if lang == 'en' else 'सामान्य' if lang == 'hi' else 'మధ్యస్థ'
        wind_icon = '💨'
    else:
        wind_status = 'light' if lang == 'en' else 'हल्की' if lang == 'hi' else 'తేలికైన'
        wind_icon = '🍃'
    
    return {
        'temp_status': temp_status,
        'temp_icon': temp_icon,
        'rain_status': rain_status,
        'rain_icon': rain_icon,
        'wind_status': wind_status,
        'wind_icon': wind_icon,
        'days_no_rain': days_no_rain,
        'needs_water': temp > 32 and days_no_rain > 7
    }
