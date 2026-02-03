"""
Configuration settings for CropGuard application
"""

# Default Map Settings
DEFAULT_LOCATION = [20.5937, 78.9629]  # Center of India
DEFAULT_ZOOM = 5
DEFAULT_AREA_KM2 = 5.0

# Sentinel Hub Settings
RESOLUTION = 10  # meters per pixel
TIME_WINDOW_DAYS = 30  # Last N days of satellite data
MOSAICKING_ORDER = 'leastCC'  # Least cloud coverage

# NDVI Classification Thresholds
NDVI_UNHEALTHY = 0.2
NDVI_MODERATE = 0.5

# Health Categories
HEALTH_CATEGORIES = {
    'unhealthy': {
        'label': 'Unhealthy',
        'color': '#FF5252',  # Vibrant Red
        'threshold': (float('-inf'), NDVI_UNHEALTHY),
        'description': 'Bare soil or stressed crops'
    },
    'moderate': {
        'label': 'Moderate',
        'color': '#FFC107',  # Vibrant Amber
        'threshold': (NDVI_UNHEALTHY, NDVI_MODERATE),
        'description': 'Sparse vegetation'
    },
    'healthy': {
        'label': 'Healthy',
        'color': '#00E676',  # Vibrant Green
        'threshold': (NDVI_MODERATE, float('inf')),
        'description': 'Dense, vigorous vegetation'
    }
}

# Evalscript for Sentinel Hub
EVALSCRIPT = """
//VERSION=3
function setup() {
  return {
    input: ["B04", "B08", "SCL"],
    output: { bands: 3, sampleType: "FLOAT32" }
  };
}

function evaluatePixel(sample) {
  return [sample.B04, sample.B08, sample.SCL];
}
"""

# Valid SCL (Scene Classification Layer) values for vegetation analysis
# 2: Dark Area Pixels, 4: Vegetation, 5: Not Vegetated, 6: Water, 7: Unclassified
VALID_SCL_VALUES = [2, 4, 5, 6, 7]

# UI Settings
APP_TITLE = "🌾 CropGuard - Crop Health Monitoring"
APP_ICON = "🌾"
SIDEBAR_STATE = "expanded"

# Map Tiles
MAP_TILES = {
    'OpenStreetMap': 'OpenStreetMap',
    'Satellite': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
}
