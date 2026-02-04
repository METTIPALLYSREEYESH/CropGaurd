"""
Disease Detection System
Detects crop diseases based on NDVI anomalies, weather conditions, and spectral signatures
"""

import numpy as np
from utils.disease_database import (
    get_diseases_for_crop,
    get_disease_by_name,
    get_all_diseases
)

def calculate_ndvi_anomaly(current_ndvi_mean, past_ndvi_mean=None, baseline_ndvi=None):
    """
    Calculate NDVI anomaly (drop from previous value)
    
    Args:
        current_ndvi_mean: Current mean NDVI value
        past_ndvi_mean: Previous mean NDVI value
        baseline_ndvi: Baseline healthy NDVI for crop
        
    Returns:
        float: NDVI drop value (0 to 1)
    """
    if past_ndvi_mean is not None:
        # If we have past data, calculate drop
        drop = max(0, past_ndvi_mean - current_ndvi_mean)
        return min(1.0, drop)
    elif baseline_ndvi is not None:
        # If we have baseline, compare to baseline
        drop = max(0, baseline_ndvi - current_ndvi_mean)
        return min(1.0, drop)
    else:
        # No reference - assume healthy if NDVI > 0.4
        if current_ndvi_mean > 0.4:
            return 0.0
        else:
            # Estimate anomaly based on absolute value
            return min(1.0, (0.4 - current_ndvi_mean) / 0.4)

def assess_weather_disease_risk(weather_data):
    """
    Assess disease risk based on weather conditions
    
    Args:
        weather_data: Dictionary with temperature, humidity, rainfall, wind
        
    Returns:
        dict: Disease risk factors
    """
    temp = weather_data.get('temperature', 20)
    humidity = weather_data.get('humidity', 50)  # Need to add this to weather API
    rainfall = weather_data.get('rainfall', 0)
    wind_speed = weather_data.get('wind_speed', 5)
    
    risk_factors = {
        'fungal_risk': 0,  # 0-100
        'bacterial_risk': 0,  # 0-100
        'favorable_conditions': [],
        'unfavorable_conditions': []
    }
    
    # Fungal diseases thrive in high humidity and moderate temperatures
    if 15 <= temp <= 28:
        risk_factors['fungal_risk'] += 30
        risk_factors['favorable_conditions'].append(f"Temperature {temp}°C (optimal for fungal growth)")
    
    if humidity >= 75:
        risk_factors['fungal_risk'] += 40
        risk_factors['favorable_conditions'].append(f"High humidity {humidity}% (fungal paradise)")
    elif humidity < 50:
        risk_factors['unfavorable_conditions'].append(f"Low humidity {humidity}% (inhibits fungi)")
    
    if rainfall > 0:
        risk_factors['fungal_risk'] += 20
        risk_factors['favorable_conditions'].append("Recent rainfall (creates leaf wetness)")
    
    # Bacterial diseases spread more in warm, wet conditions
    if 25 <= temp <= 35 and humidity >= 80:
        risk_factors['bacterial_risk'] += 50
        risk_factors['favorable_conditions'].append("Warm + humid (bacterial spread conditions)")
    
    # Wind can help reduce disease risk by drying leaves
    if wind_speed > 10:
        risk_factors['fungal_risk'] -= 15
        risk_factors['bacterial_risk'] -= 10
        risk_factors['unfavorable_conditions'].append(f"Strong wind {wind_speed} km/h (dries leaves)")
    
    # Cap values at 0-100
    risk_factors['fungal_risk'] = max(0, min(100, risk_factors['fungal_risk']))
    risk_factors['bacterial_risk'] = max(0, min(100, risk_factors['bacterial_risk']))
    
    return risk_factors

def detect_diseases(current_ndvi_mean, past_ndvi_mean, detected_crop, weather_data, confidence_threshold=0.5):
    """
    Detect potential diseases in a field
    
    Args:
        current_ndvi_mean: Current mean NDVI
        past_ndvi_mean: Past mean NDVI
        detected_crop: Detected crop name
        weather_data: Weather information
        confidence_threshold: Minimum confidence to report disease (0-1)
        
    Returns:
        dict: Disease detections with confidence and severity
    """
    
    # Get possible diseases for the crop
    possible_diseases = get_diseases_for_crop(detected_crop)
    
    if not possible_diseases:
        return {
            'detected_diseases': [],
            'disease_risk_level': 'Low',
            'weather_risk_summary': {},
            'recommendations': []
        }
    
    # Calculate NDVI anomaly
    ndvi_anomaly = calculate_ndvi_anomaly(current_ndvi_mean, past_ndvi_mean)
    
    # Get weather-based disease risk
    weather_risk = assess_weather_disease_risk(weather_data)
    
    detected_diseases = []
    
    # Check each possible disease
    for disease_name, disease_info in possible_diseases:
        confidence = 0.0
        severity = 'None'
        
        # Factor 1: NDVI drop indicator (40% weight)
        ndvi_threshold = disease_info['indicators']['ndvi_drop']
        if ndvi_anomaly >= ndvi_threshold:
            confidence += 0.40
            # Estimate severity based on how much it exceeds threshold
            severity_ratio = min(1.0, ndvi_anomaly / (ndvi_threshold * 2))
            if severity_ratio >= 0.6:
                severity = 'Severe'
            elif severity_ratio >= 0.3:
                severity = 'Moderate'
            else:
                severity = 'Mild'
        
        # Factor 2: Temperature match (25% weight)
        temp = weather_data.get('temperature', 20)
        temp_min, temp_max = disease_info['indicators']['optimal_temp']
        if temp_min <= temp <= temp_max:
            confidence += 0.25
        
        # Factor 3: Humidity match (25% weight) - if available
        humidity = weather_data.get('humidity', 50)
        hum_min, hum_max = disease_info['indicators']['optimal_humidity']
        if hum_min <= humidity <= hum_max:
            confidence += 0.25
        
        # Factor 4: Type-based weather risk (10% bonus)
        if 'fungal' in disease_name.lower() and weather_risk['fungal_risk'] > 60:
            confidence += 0.10
        elif 'bacterial' in disease_name.lower() and weather_risk['bacterial_risk'] > 60:
            confidence += 0.10
        
        confidence = min(1.0, confidence)
        
        # Only include if above threshold
        if confidence >= confidence_threshold:
            detected_diseases.append({
                'disease_name': disease_name,
                'confidence': confidence,
                'severity': severity if severity != 'None' else 'Mild',
                'indicators': disease_info['indicators'],
                'treatments': disease_info['treatments'],
                'prevention': disease_info['prevention'],
                'description': disease_info['description'],
                'local_names': disease_info['local_names']
            })
    
    # Sort by confidence
    detected_diseases.sort(key=lambda x: x['confidence'], reverse=True)
    
    # Determine overall disease risk level
    if detected_diseases:
        avg_confidence = np.mean([d['confidence'] for d in detected_diseases])
        if avg_confidence >= 0.8:
            disease_risk_level = 'Critical'
        elif avg_confidence >= 0.6:
            disease_risk_level = 'High'
        else:
            disease_risk_level = 'Moderate'
    else:
        disease_risk_level = 'Low'
    
    # Generate recommendations
    recommendations = []
    if disease_risk_level in ['Critical', 'High']:
        recommendations.append(f"🚨 Disease risk is {disease_risk_level}. Consider preventive measures immediately.")
    
    if weather_risk['favorable_conditions']:
        recommendations.append(f"⚠️ Current conditions favor disease: {', '.join(weather_risk['favorable_conditions'][:2])}")
    
    if detected_diseases:
        top_disease = detected_diseases[0]
        recommendations.append(f"🔬 Top concern: {top_disease['disease_name']} ({top_disease['severity']})")
    
    return {
        'detected_diseases': detected_diseases[:5],  # Top 5 diseases
        'disease_risk_level': disease_risk_level,
        'weather_risk_summary': weather_risk,
        'recommendations': recommendations,
        'ndvi_anomaly': float(ndvi_anomaly)
    }

def get_disease_severity_color(severity):
    """Get color for disease severity level"""
    colors = {
        'Mild': '#FFC107',        # Yellow
        'Moderate': '#FF9800',    # Orange
        'Severe': '#F44336',      # Red
    }
    return colors.get(severity, '#999999')

def get_disease_risk_color(risk_level):
    """Get color for disease risk level"""
    colors = {
        'Low': '#4CAF50',         # Green
        'Moderate': '#FFC107',    # Yellow
        'High': '#FF9800',        # Orange
        'Critical': '#F44336'     # Red
    }
    return colors.get(risk_level, '#999999')

def format_disease_report(disease_detection):
    """Format disease detection results for display"""
    report = {
        'summary': f"Disease Risk: {disease_detection['disease_risk_level']}",
        'diseases': [],
        'actions': disease_detection['recommendations']
    }
    
    for disease in disease_detection['detected_diseases']:
        report['diseases'].append({
            'name': disease['disease_name'],
            'confidence': f"{disease['confidence']*100:.0f}%",
            'severity': disease['severity'],
            'description': disease['description'],
            'treatments': disease['treatments'],
            'prevention': disease['prevention']
        })
    
    return report
