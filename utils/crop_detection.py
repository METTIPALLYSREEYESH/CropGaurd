"""
Rule-Based Crop Inference Engine.
Guesses crop type based on location, time, and NDVI signature.
Note: Simplified for Hackathon Demo purposes.
"""
import datetime

def detect_crop(mean_ndvi, month_index):
    """
    Infer potential crop type based on simple seasonal rules.
    
    Args:
        mean_ndvi (float): Average NDVI of the area.
        month_index (int): Month number (1-12).
        
    Returns:
        tuple: (Crop Name, Confidence Level)
    """
    
    # Very basic seasonal logic for India/Southeast Asia context
    # Rabi Season (Winter): Wheat, Mustard (Nov - Apr)
    # Kharif Season (Monsoon): Rice, Maize (Jun - Oct)
    
    is_kharif = 6 <= month_index <= 10
    is_rabi = month_index >= 11 or month_index <= 4
    
    crop_name = "Unknown Vegetation"
    confidence = "Low"
    
    if mean_ndvi < 0.2:
        return "Fallow / Bare Soil", "High"
        
    if is_kharif:
        if mean_ndvi > 0.6:
            crop_name = "Rice (Paddy)"
            confidence = "Medium"
        elif mean_ndvi > 0.4:
            crop_name = "Maize / Cotton"
            confidence = "Low"
        else:
             crop_name = "Early Growth Stage"
             confidence = "Low"
             
    elif is_rabi:
        if mean_ndvi > 0.5:
            crop_name = "Wheat"
            confidence = "Medium"
        elif mean_ndvi > 0.35:
            crop_name = "Mustard / Gram"
            confidence = "Low"
    
    return crop_name, confidence
