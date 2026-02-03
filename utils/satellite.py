"""
Sentinel Hub data fetching utilities
"""
import datetime
import numpy as np
from sentinelhub import (
    SHConfig,
    SentinelHubRequest,
    DataCollection,
    MimeType,
    CRS,
    BBox,
    bbox_to_dimensions
)
from config import EVALSCRIPT, RESOLUTION, TIME_WINDOW_DAYS, MOSAICKING_ORDER


def create_config(client_id, client_secret):
    """
    Create Sentinel Hub configuration
    
    Args:
        client_id: OAuth client ID
        client_secret: OAuth client secret
        
    Returns:
        SHConfig object or None if invalid
    """
    if not client_id or not client_secret or 'your_' in client_id.lower():
        return None
    
    config = SHConfig()
    config.sh_client_id = client_id
    config.sh_client_secret = client_secret
    return config


def create_bbox_from_center(lat, lon, km2):
    """
    Creates a BBox around a center point with approximate area size
    
    Args:
        lat: Latitude of center point
        lon: Longitude of center point
        km2: Approximate area in square kilometers
        
    Returns:
        BBox object
    """
    side_length_km = np.sqrt(km2)
    half_side = side_length_km / 2
    
    # Approximate conversion (1 degree lat ~ 111 km)
    lat_deg = half_side / 111.0
    lon_deg = half_side / (111.0 * np.cos(np.radians(lat)))
    
    return BBox(
        bbox=[lon - lon_deg, lat - lat_deg, lon + lon_deg, lat + lat_deg],
        crs=CRS.WGS84
    )


def create_bbox_from_geojson(geojson_data):
    """
    Create BBox from GeoJSON geometry
    
    Args:
        geojson_data: GeoJSON dict with geometry
        
    Returns:
        BBox object or None
    """
    try:
        from shapely.geometry import shape
        
        # Handle FeatureCollection
        if geojson_data.get('type') == 'FeatureCollection':
            features = geojson_data.get('features', [])
            if features:
                geom = features[0]['geometry']
            else:
                return None
        elif geojson_data.get('type') == 'Feature':
            geom = geojson_data['geometry']
        else:
            geom = geojson_data
        
        # Create shapely geometry and get bounds
        poly = shape(geom)
        bounds = poly.bounds  # (minx, miny, maxx, maxy)
        
        return BBox(bbox=bounds, crs=CRS.WGS84)
    except Exception as e:
        print(f"Error parsing GeoJSON: {e}")
        return None


def fetch_satellite_data(config, bbox, time_interval=None):
    """
    Fetch Sentinel-2 L2A data from Sentinel Hub
    
    Args:
        config: SHConfig object
        bbox: BBox object defining area of interest
        time_interval: Tuple of (start_date, end_date) strings
        
    Returns:
        NumPy array of shape (time, height, width, bands) or None
    """
    try:
        # Default time interval: last 30 days
        if time_interval is None:
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=TIME_WINDOW_DAYS)
            time_interval = (
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d')
            )
        
        # Calculate image size
        size = bbox_to_dimensions(bbox, resolution=RESOLUTION)
        
        # Create request
        request = SentinelHubRequest(
            evalscript=EVALSCRIPT,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L2A,
                    time_interval=time_interval,
                    mosaicking_order=MOSAICKING_ORDER
                )
            ],
            responses=[
                SentinelHubRequest.output_response('default', MimeType.TIFF)
            ],
            bbox=bbox,
            size=size,
            config=config
        )
        
        # Fetch data
        data = request.get_data()
        
        if len(data) == 0:
            return None
            
        return np.array(data)
        
    except Exception as e:
        raise Exception(f"Error fetching satellite data: {str(e)}")


def get_bbox_info(bbox):
    """
    Get information about a bounding box
    
    Args:
        bbox: BBox object
        
    Returns:
        Dict with bbox information
    """
    # Calculate approximate area
    lat_range = bbox.max_y - bbox.min_y
    lon_range = bbox.max_x - bbox.min_x
    
    # Approximate area in km²
    lat_km = lat_range * 111
    lon_km = lon_range * 111 * np.cos(np.radians((bbox.min_y + bbox.max_y) / 2))
    area_km2 = lat_km * lon_km
    
    return {
        'min_lat': bbox.min_y,
        'max_lat': bbox.max_y,
        'min_lon': bbox.min_x,
        'max_lon': bbox.max_x,
        'center_lat': (bbox.min_y + bbox.max_y) / 2,
        'center_lon': (bbox.min_x + bbox.max_x) / 2,
        'area_km2': area_km2
    }
