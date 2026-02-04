"""
Crop Recommendation System
Recommends suitable crops based on weather, soil health, and location
"""

import numpy as np

# Crop database with growing requirements
CROP_DATABASE = {
    'Rice': {
        'temp_range': (20, 35),
        'temp_optimal': (25, 30),
        'rainfall_min': 1000,  # mm/year
        'soil_moisture': 'high',
        'ndvi_min': 0.3,
        'season': ['Kharif', 'Rabi'],
        'water_requirement': 'very_high',
        'soil_type': ['clay', 'loamy'],
        'regions': ['coastal', 'plains', 'delta'],
        'icon': '🌾',
        'local_names': {
            'en': 'Rice',
            'hi': 'धान',
            'te': 'వరి'
        }
    },
    'Wheat': {
        'temp_range': (10, 25),
        'temp_optimal': (15, 20),
        'rainfall_min': 400,
        'soil_moisture': 'medium',
        'ndvi_min': 0.4,
        'season': ['Rabi'],
        'water_requirement': 'medium',
        'soil_type': ['loamy', 'clay'],
        'regions': ['plains', 'plateau'],
        'icon': '🌾',
        'local_names': {
            'en': 'Wheat',
            'hi': 'गेहूं',
            'te': 'గోధుమ'
        }
    },
    'Cotton': {
        'temp_range': (21, 35),
        'temp_optimal': (25, 32),
        'rainfall_min': 600,
        'soil_moisture': 'medium',
        'ndvi_min': 0.35,
        'season': ['Kharif'],
        'water_requirement': 'medium',
        'soil_type': ['black', 'loamy'],
        'regions': ['plateau', 'plains'],
        'icon': '☁️',
        'local_names': {
            'en': 'Cotton',
            'hi': 'कपास',
            'te': 'పత్తి'
        }
    },
    'Sugarcane': {
        'temp_range': (20, 35),
        'temp_optimal': (25, 32),
        'rainfall_min': 1500,
        'soil_moisture': 'high',
        'ndvi_min': 0.5,
        'season': ['Year-round'],
        'water_requirement': 'very_high',
        'soil_type': ['loamy', 'clay'],
        'regions': ['plains', 'coastal'],
        'icon': '🎋',
        'local_names': {
            'en': 'Sugarcane',
            'hi': 'गन्ना',
            'te': 'చెరకు'
        }
    },
    'Maize': {
        'temp_range': (18, 32),
        'temp_optimal': (21, 27),
        'rainfall_min': 500,
        'soil_moisture': 'medium',
        'ndvi_min': 0.4,
        'season': ['Kharif', 'Rabi'],
        'water_requirement': 'medium',
        'soil_type': ['loamy', 'sandy'],
        'regions': ['plains', 'hills'],
        'icon': '🌽',
        'local_names': {
            'en': 'Maize',
            'hi': 'मक्का',
            'te': 'మొక్కజొన్న'
        }
    },
    'Soybean': {
        'temp_range': (20, 30),
        'temp_optimal': (22, 28),
        'rainfall_min': 450,
        'soil_moisture': 'medium',
        'ndvi_min': 0.35,
        'season': ['Kharif'],
        'water_requirement': 'low',
        'soil_type': ['loamy', 'black'],
        'regions': ['plateau', 'plains'],
        'icon': '🫘',
        'local_names': {
            'en': 'Soybean',
            'hi': 'सोयाबीन',
            'te': 'సోయాబీన్'
        }
    },
    'Groundnut': {
        'temp_range': (20, 30),
        'temp_optimal': (22, 28),
        'rainfall_min': 500,
        'soil_moisture': 'low',
        'ndvi_min': 0.3,
        'season': ['Kharif', 'Rabi'],
        'water_requirement': 'low',
        'soil_type': ['sandy', 'loamy'],
        'regions': ['plains', 'coastal'],
        'icon': '🥜',
        'local_names': {
            'en': 'Groundnut',
            'hi': 'मूंगफली',
            'te': 'వేరుశెనగ'
        }
    },
    'Chickpea': {
        'temp_range': (10, 25),
        'temp_optimal': (15, 22),
        'rainfall_min': 400,
        'soil_moisture': 'low',
        'ndvi_min': 0.3,
        'season': ['Rabi'],
        'water_requirement': 'low',
        'soil_type': ['loamy', 'black'],
        'regions': ['plateau', 'plains'],
        'icon': '🫘',
        'local_names': {
            'en': 'Chickpea',
            'hi': 'चना',
            'te': 'శనగలు'
        }
    },
    'Tomato': {
        'temp_range': (15, 30),
        'temp_optimal': (20, 25),
        'rainfall_min': 600,
        'soil_moisture': 'medium',
        'ndvi_min': 0.4,
        'season': ['Year-round'],
        'water_requirement': 'medium',
        'soil_type': ['loamy', 'sandy'],
        'regions': ['plains', 'hills'],
        'icon': '🍅',
        'local_names': {
            'en': 'Tomato',
            'hi': 'टमाटर',
            'te': 'టమోటా'
        }
    },
    'Onion': {
        'temp_range': (13, 28),
        'temp_optimal': (18, 24),
        'rainfall_min': 650,
        'soil_moisture': 'medium',
        'ndvi_min': 0.35,
        'season': ['Rabi'],
        'water_requirement': 'medium',
        'soil_type': ['loamy', 'sandy'],
        'regions': ['plains', 'plateau'],
        'icon': '🧅',
        'local_names': {
            'en': 'Onion',
            'hi': 'प्याज',
            'te': 'ఉల్లిపాయ'
        }
    }
}

def get_region_from_coordinates(lat, lon):
    """
    Determine region type from coordinates
    Simple heuristic based on Indian geography
    """
    # Coastal regions (near coast)
    if (lat < 20 and lon > 80) or (lat < 15 and lon < 80):
        return 'coastal'
    # Plateau regions (Deccan)
    elif 15 < lat < 20 and 75 < lon < 80:
        return 'plateau'
    # Delta regions
    elif 10 < lat < 15 and 78 < lon < 82:
        return 'delta'
    # Hills (North)
    elif lat > 28:
        return 'hills'
    # Default to plains
    else:
        return 'plains'

def calculate_soil_health_from_ndvi(ndvi_mean):
    """
    Estimate soil health from NDVI
    """
    if ndvi_mean > 0.6:
        return 'excellent'
    elif ndvi_mean > 0.4:
        return 'good'
    elif ndvi_mean > 0.2:
        return 'moderate'
    else:
        return 'poor'

def recommend_crops(weather_data, ndvi_mean, latitude, longitude, current_season='Kharif'):
    """
    Recommend suitable crops based on conditions
    
    Args:
        weather_data (dict): Weather data from fetch_weather_data
        ndvi_mean (float): Mean NDVI value of field
        latitude (float): Field latitude
        longitude (float): Field longitude
        current_season (str): Current growing season
        
    Returns:
        list: List of recommended crops with suitability scores
    """
    temperature = weather_data['temperature']
    days_since_rain = weather_data['days_since_rain']
    region = get_region_from_coordinates(latitude, longitude)
    soil_health = calculate_soil_health_from_ndvi(ndvi_mean)
    
    recommendations = []
    
    for crop_name, crop_info in CROP_DATABASE.items():
        score = 0
        reasons = []
        warnings = []
        
        # Temperature suitability (40 points)
        temp_min, temp_max = crop_info['temp_range']
        temp_opt_min, temp_opt_max = crop_info['temp_optimal']
        
        if temp_opt_min <= temperature <= temp_opt_max:
            score += 40
            reasons.append("Optimal temperature")
        elif temp_min <= temperature <= temp_max:
            score += 25
            reasons.append("Suitable temperature")
        else:
            score += 0
            warnings.append(f"Temperature not ideal ({temp_min}-{temp_max}°C needed)")
        
        # Water availability (25 points)
        if crop_info['water_requirement'] == 'very_high':
            if days_since_rain < 3:
                score += 25
                reasons.append("Good water availability")
            else:
                score += 10
                warnings.append("Needs frequent irrigation")
        elif crop_info['water_requirement'] == 'medium':
            if days_since_rain < 7:
                score += 25
                reasons.append("Adequate water")
            else:
                score += 15
                warnings.append("May need irrigation")
        else:  # low
            score += 25
            reasons.append("Low water requirement")
        
        # Soil health (20 points)
        if ndvi_mean >= crop_info['ndvi_min']:
            score += 20
            reasons.append("Soil health suitable")
        else:
            score += 5
            warnings.append("Soil may need improvement")
        
        # Region suitability (10 points)
        if region in crop_info['regions']:
            score += 10
            reasons.append(f"Suitable for {region} region")
        else:
            score += 3
        
        # Season suitability (5 points)
        if current_season in crop_info['season'] or 'Year-round' in crop_info['season']:
            score += 5
            reasons.append(f"Good for {current_season} season")
        else:
            warnings.append(f"Not ideal for {current_season} season")
        
        recommendations.append({
            'name': crop_name,
            'score': score,
            'suitability': get_suitability_level(score),
            'icon': crop_info['icon'],
            'local_names': crop_info['local_names'],
            'reasons': reasons,
            'warnings': warnings,
            'water_req': crop_info['water_requirement'],
            'season': crop_info['season']
        })
    
    # Sort by score (highest first)
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    return recommendations

def get_suitability_level(score):
    """Get suitability level from score"""
    if score >= 80:
        return 'Highly Suitable'
    elif score >= 60:
        return 'Suitable'
    elif score >= 40:
        return 'Moderately Suitable'
    else:
        return 'Not Recommended'

def get_suitability_color(level):
    """Get color for suitability level"""
    colors = {
        'Highly Suitable': '#16a34a',
        'Suitable': '#10b981',
        'Moderately Suitable': '#f59e0b',
        'Not Recommended': '#dc2626'
    }
    return colors.get(level, '#6b7280')
