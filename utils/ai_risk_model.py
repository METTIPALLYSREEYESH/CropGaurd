"""
AI Risk Model for Early Crop Stress Detection
Encapsulates logic for calculating risk, generating explanations, and computing AI scores.
"""

def calculate_ndvi_change(current_ndvi_mean, past_ndvi_mean):
    """
    Calculate the change in NDVI.
    
    Args:
        current_ndvi_mean (float): Mean NDVI of the recent period.
        past_ndvi_mean (float): Mean NDVI of the past period.
        
    Returns:
        float: The change in NDVI (current - past).
    """
    if current_ndvi_mean is None or past_ndvi_mean is None:
        return 0.0
    return current_ndvi_mean - past_ndvi_mean


def assess_risk(ndvi_change):
    """
    Classify crop stress risk based on NDVI change.
    
    Rule-based Logic:
    - NDVI Improvement or minor decline (> -0.05) -> Stable
    - Moderate decline (-0.05 to -0.15) -> Medium Risk
    - Sharp decline (< -0.15) -> High Risk
    
    Args:
        ndvi_change (float): The calculated change in NDVI.
        
    Returns:
        str: 'High Risk', 'Medium Risk', or 'Stable'
    """
    if ndvi_change < -0.15:
        return 'High Risk'
    elif ndvi_change < -0.05:
        return 'Medium Risk'
    else:
        return 'Stable'


def get_risk_explanation(risk_level, weather_context=None):
    """
    Generate a human-readable explanation for the risk level, enriched with weather data.
    
    Args:
        risk_level (str): The classification ('High Risk', 'Medium Risk', 'Stable').
        weather_context (dict, optional): Weather info {temp, humidity, rain_status}.
        
    Returns:
        str: A descriptive explanation of the potential cause and status.
    """
    explanation = ""
    weather_note = ""
    
    # Analyze weather context if available
    if weather_context and weather_context.get('temp') != "--":
        temp = float(weather_context['temp'])
        humidity = float(weather_context['humidity'])
        
        if temp > 35 and humidity < 40:
            weather_note = " combined with high heat and low humidity (Drought Risk)."
        elif weather_context.get('rain_status') == 'Heavy Rain':
            weather_note = " possibly linked to waterlogging due to heavy rain."
            
    if risk_level == 'High Risk':
        explanation = f"⚠️ Significant vegetation decline detected{weather_note}. Potential causes include severe water stress, pest infestation, or disease outbreak. Immediate inspection recommended."
    elif risk_level == 'Medium Risk':
        if weather_note:
             explanation = f"⚠️ Early signs of stress detected{weather_note}. Vegetation vigor is slightly lower than expected."
        else:
             explanation = "⚠️ Early signs of stress detected. Vegetation vigor is slightly lower than previous weeks. Monitor soil moisture and check for early pest signs."
    else:
        explanation = "✅ Crop condition is stable or improving. No significant stress anomalies detected compared to the previous period."
        
    return explanation


def get_action_recommendation(risk_level):
    """
    Generate actionable advice for farmers based on risk level.
    
    Args:
        risk_level (str): 'High Risk', 'Medium Risk', 'Stable'
    
    Returns:
        str: Specific action recommendation.
    """
    if risk_level == 'High Risk':
        return "🚨 **URGENT**: Increase irrigation immediately and inspect field for pest/disease outbreaks."
    elif risk_level == 'Medium Risk':
        return "👀 **Advice**: Monitor soil moisture closely and check for early signs of yellowing."
    else:
        return "✅ **Advice**: Maintain current care schedule. No immediate action required."


def calculate_ai_score(risk_level, current_ndvi_mean):
    """
    Compute an 'AI Health Score' (0-100) based on risk and current health.
    
    Args:
        risk_level (str): 'High Risk', 'Medium Risk', 'Stable'
        current_ndvi_mean (float): The current NDVI mean (0.0 to 1.0 typical range)
        
    Returns:
        int: Score between 0 and 100.
    """
    base_score = 0
    
    # Establish base range based on risk
    if risk_level == 'Stable':
        base_score = 90
    elif risk_level == 'Medium Risk':
        base_score = 65
    else:  # High Risk
        base_score = 40
        
    # Adjust slightly based on actual NDVI value (higher NDVI is generally better)
    # NDVI is typically 0.2 to 0.8 for vegetation.
    # We add up to 10 points for healthy vegetation, subtract for very low.
    
    ndvi_adjustment = 0
    if current_ndvi_mean > 0.6:
        ndvi_adjustment = 10
    elif current_ndvi_mean > 0.4:
        ndvi_adjustment = 5
    elif current_ndvi_mean < 0.2:
        ndvi_adjustment = -10
        
    final_score = base_score + ndvi_adjustment
    
    # Clamp between 0 and 100
    return max(0, min(100, int(final_score)))
