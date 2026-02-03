"""
NDVI computation and crop health classification
"""
import numpy as np
from config import VALID_SCL_VALUES, HEALTH_CATEGORIES


def compute_ndvi(data_array):
    """
    Compute NDVI from satellite data with cloud masking
    
    Args:
        data_array: NumPy array of shape (time, height, width, 3)
                   Bands: [B04 (Red), B08 (NIR), SCL]
    
    Returns:
        2D NumPy array of temporally averaged NDVI values
    """
    ndvi_list = []
    
    for image in data_array:
        red = image[:, :, 0]
        nir = image[:, :, 1]
        scl = image[:, :, 2]
        
        # Create mask for valid pixels (vegetation, soil, water)
        valid_mask = np.isin(scl, VALID_SCL_VALUES)
        
        # Compute NDVI: (NIR - Red) / (NIR + Red)
        denominator = (nir + red)
        denominator[denominator == 0] = 0.0001  # Avoid division by zero
        
        ndvi = (nir - red) / denominator
        
        # Apply cloud mask
        ndvi_cleaned = np.where(valid_mask, ndvi, np.nan)
        
        # Clip to valid NDVI range [-1, 1]
        ndvi_cleaned = np.clip(ndvi_cleaned, -1, 1)
        
        ndvi_list.append(ndvi_cleaned)
    
    # Temporal averaging (ignore NaN values from clouds)
    ndvi_avg = np.nanmean(np.array(ndvi_list), axis=0)
    
    return ndvi_avg


def classify_health(ndvi_map):
    """
    Classify NDVI values into health categories
    
    Args:
        ndvi_map: 2D NumPy array of NDVI values
        
    Returns:
        Dict with classification results
    """
    valid_ndvi = ndvi_map[~np.isnan(ndvi_map)]
    
    if len(valid_ndvi) == 0:
        return None
    
    # Count pixels in each category
    unhealthy_mask = ndvi_map < HEALTH_CATEGORIES['unhealthy']['threshold'][1]
    moderate_mask = (
        (ndvi_map >= HEALTH_CATEGORIES['moderate']['threshold'][0]) &
        (ndvi_map < HEALTH_CATEGORIES['moderate']['threshold'][1])
    )
    healthy_mask = ndvi_map >= HEALTH_CATEGORIES['healthy']['threshold'][0]
    
    unhealthy_count = np.sum(unhealthy_mask)
    moderate_count = np.sum(moderate_mask)
    healthy_count = np.sum(healthy_mask)
    total_count = unhealthy_count + moderate_count + healthy_count
    
    return {
        'unhealthy': {
            'count': int(unhealthy_count),
            'percentage': float(unhealthy_count / total_count * 100) if total_count > 0 else 0
        },
        'moderate': {
            'count': int(moderate_count),
            'percentage': float(moderate_count / total_count * 100) if total_count > 0 else 0
        },
        'healthy': {
            'count': int(healthy_count),
            'percentage': float(healthy_count / total_count * 100) if total_count > 0 else 0
        },
        'total_pixels': int(total_count),
        'statistics': {
            'mean': float(np.nanmean(valid_ndvi)),
            'std': float(np.nanstd(valid_ndvi)),
            'min': float(np.nanmin(valid_ndvi)),
            'max': float(np.nanmax(valid_ndvi)),
            'median': float(np.nanmedian(valid_ndvi))
        }
    }


def create_health_mask(ndvi_map):
    """
    Create RGB image for health visualization
    
    Args:
        ndvi_map: 2D NumPy array of NDVI values
        
    Returns:
        RGBA image array (height, width, 4)
    """
    h, w = ndvi_map.shape
    rgba_img = np.zeros((h, w, 4), dtype=np.uint8)
    
    # Assign colors based on health categories
    for category_name, category_info in HEALTH_CATEGORIES.items():
        color_hex = category_info['color']
        # Convert hex to RGB
        r = int(color_hex[1:3], 16)
        g = int(color_hex[3:5], 16)
        b = int(color_hex[5:7], 16)
        
        min_val, max_val = category_info['threshold']
        
        if category_name == 'unhealthy':
            mask = ndvi_map < max_val
        elif category_name == 'moderate':
            mask = (ndvi_map >= min_val) & (ndvi_map < max_val)
        else:  # healthy
            mask = ndvi_map >= min_val
        
        rgba_img[mask] = [r, g, b, 200]
    
    # Make NaN pixels transparent
    rgba_img[np.isnan(ndvi_map)] = [0, 0, 0, 0]
    
    return rgba_img


def get_ndvi_description(ndvi_value):
    """
    Get health description for a specific NDVI value
    
    Args:
        ndvi_value: Float NDVI value
        
    Returns:
        String description
    """
    for category_name, category_info in HEALTH_CATEGORIES.items():
        min_val, max_val = category_info['threshold']
        if min_val <= ndvi_value < max_val:
            return f"{category_info['label']}: {category_info['description']}"
    
    return "Unknown"
