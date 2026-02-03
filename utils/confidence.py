"""
AI Confidence Score Calculator
Determines prediction reliability based on data quality
"""
import numpy as np

def calculate_confidence(ndvi_map, cloud_cover_pct=0):
    """
    Calculate AI prediction confidence based on data quality.
    
    Args:
        ndvi_map (np.array): NDVI data array
        cloud_cover_pct (float): Cloud cover percentage (0-100)
        
    Returns:
        str: 'High', 'Medium', or 'Low'
    """
    # Calculate NDVI variance (consistency indicator)
    valid_ndvi = ndvi_map[~np.isnan(ndvi_map)]
    
    if len(valid_ndvi) == 0:
        return 'Low'
    
    variance = float(np.var(valid_ndvi))
    
    # Calculate data completeness (% of non-NaN pixels)
    total_pixels = ndvi_map.size
    valid_pixels = len(valid_ndvi)
    data_completeness = valid_pixels / total_pixels
    
    # Confidence logic
    # High confidence: Low variance + high completeness + low cloud cover
    if variance < 0.05 and data_completeness > 0.8 and cloud_cover_pct < 20:
        return 'High'
    
    # Medium confidence: Moderate variance or completeness
    elif variance < 0.15 and data_completeness > 0.5 and cloud_cover_pct < 40:
        return 'Medium'
    
    # Low confidence: High variance, low completeness, or high cloud cover
    else:
        return 'Low'

def get_confidence_color(confidence):
    """
    Get color code for confidence level.
    
    Args:
        confidence (str): 'High', 'Medium', or 'Low'
        
    Returns:
        str: Hex color code
    """
    colors = {
        'High': '#4CAF50',    # Green
        'Medium': '#FF9800',  # Orange
        'Low': '#F44336'      # Red
    }
    return colors.get(confidence, '#757575')

def get_confidence_icon(confidence):
    """
    Get emoji icon for confidence level.
    
    Args:
        confidence (str): 'High', 'Medium', or 'Low'
        
    Returns:
        str: Emoji icon
    """
    icons = {
        'High': '✓',
        'Medium': '~',
        'Low': '!'
    }
    return icons.get(confidence, '?')
