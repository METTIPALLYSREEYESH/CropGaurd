"""
Field Manager - Save and load field locations with analysis history
"""
import json
import os
from datetime import datetime

FIELDS_FILE = "data/saved_fields.json"

def ensure_data_dir():
    """Create data directory if it doesn't exist"""
    os.makedirs("data", exist_ok=True)

def save_field(name, bbox, ai_results, detected_crop):
    """
    Save a field with its latest analysis results.
    
    Args:
        name (str): Field name
        bbox: BBox object with coordinates
        ai_results (dict): Latest AI analysis
        detected_crop (str): Detected crop type
    """
    ensure_data_dir()
    
    # Load existing fields
    fields = load_fields()
    
    # Create field entry
    fields[name] = {
        "bbox": {
            "min_x": bbox.min_x,
            "min_y": bbox.min_y,
            "max_x": bbox.max_x,
            "max_y": bbox.max_y
        },
        "last_analysis": {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "risk_level": ai_results.get('risk_level', 'Unknown'),
            "ai_score": ai_results.get('ai_score', 0),
            "detected_crop": detected_crop
        }
    }
    
    # Save to file
    with open(FIELDS_FILE, 'w') as f:
        json.dump(fields, f, indent=2)
    
    return True

def load_fields():
    """
    Load all saved fields.
    
    Returns:
        dict: Dictionary of saved fields
    """
    ensure_data_dir()
    
    if not os.path.exists(FIELDS_FILE):
        return {}
    
    try:
        with open(FIELDS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def delete_field(name):
    """
    Delete a saved field.
    
    Args:
        name (str): Field name to delete
    """
    fields = load_fields()
    if name in fields:
        del fields[name]
        with open(FIELDS_FILE, 'w') as f:
            json.dump(fields, f, indent=2)
        return True
    return False

def get_field_bbox(name):
    """
    Get bbox coordinates for a saved field.
    
    Args:
        name (str): Field name
        
    Returns:
        dict: Bbox coordinates or None
    """
    fields = load_fields()
    if name in fields:
        return fields[name]['bbox']
    return None
