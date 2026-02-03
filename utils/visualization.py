"""
Visualization utilities for maps and charts
"""
import folium
from folium.plugins import Draw, Geocoder, LocateControl, Fullscreen
import matplotlib.pyplot as plt
import numpy as np
from config import DEFAULT_LOCATION, DEFAULT_ZOOM, MAP_TILES, HEALTH_CATEGORIES


def create_base_map(location=None, zoom=None):
    """
    Create base Folium map with interactive features
    
    Args:
        location: [lat, lon] for map center
        zoom: Initial zoom level
        
    Returns:
        Folium Map object
    """
    if location is None:
        location = DEFAULT_LOCATION
    if zoom is None:
        zoom = DEFAULT_ZOOM
    
    # Create map
    m = folium.Map(
        location=location,
        zoom_start=zoom,
        tiles='OpenStreetMap'
    )
    
    # Add satellite imagery layer
    folium.TileLayer(
        tiles=MAP_TILES['Satellite'],
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add location control (GPS)
    LocateControl(
        auto_start=False,
        position='topleft',
        strings={
            'title': 'Show my location',
            'popup': 'You are here!'
        }
    ).add_to(m)
    
    # Add geocoder (search)
    Geocoder(
        collapsed=False,
        position='topright',
        placeholder='Search for a location...'
    ).add_to(m)
    
    # Add drawing tools
    draw = Draw(
        export=True,
        filename='area_of_interest.geojson',
        position='topleft',
        draw_options={
            'polyline': False,
            'polygon': {
                'allowIntersection': False,
                'drawError': {
                    'color': '#e1e100',
                    'message': '<strong>Error:</strong> Shape edges cannot cross!'
                },
                'shapeOptions': {
                    'color': '#00ff00',
                    'fillOpacity': 0.3
                }
            },
            'circle': False,
            'rectangle': {
                'shapeOptions': {
                    'color': '#00ff00',
                    'fillOpacity': 0.3
                }
            },
            'marker': False,
            'circlemarker': False,
        },
        edit_options={
            'edit': True,
            'remove': True
        }
    )
    draw.add_to(m)
    
    # Add fullscreen
    Fullscreen(
        position='topright',
        title='Fullscreen',
        title_cancel='Exit fullscreen',
        force_separate_button=True
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m


def create_result_map(ndvi_map, bbox, classification_results):
    """
    Create map with NDVI overlay and results
    
    Args:
        ndvi_map: 2D NumPy array of NDVI values
        bbox: BBox object
        classification_results: Dict from classify_health()
        
    Returns:
        Folium Map object
    """
    from utils.ndvi import create_health_mask
    
    # Create colored overlay
    rgba_img = create_health_mask(ndvi_map)
    
    # Create map centered on bbox
    center_lat = (bbox.min_y + bbox.max_y) / 2
    center_lon = (bbox.min_x + bbox.max_x) / 2
    
    result_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=14,
        tiles='OpenStreetMap'
    )
    
    # Add satellite layer
    folium.TileLayer(
        tiles=MAP_TILES['Satellite'],
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(result_map)
    
    # Add NDVI overlay
    img_overlay = folium.raster_layers.ImageOverlay(
        name='NDVI Health Map',
        image=rgba_img,
        bounds=[[bbox.min_y, bbox.min_x], [bbox.max_y, bbox.max_x]],
        opacity=0.7,
        interactive=True,
        cross_origin=False,
        zindex=1
    )
    img_overlay.add_to(result_map)
    
    # Create legend
    stats = classification_results['statistics']
    legend_html = f'''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 280px;
     border: 3px solid #4CAF50; z-index: 9999; font-size: 14px;
     background-color: white; opacity: 0.95; padding: 15px;
     border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
     <h4 style="margin: 0 0 10px 0; color: #4CAF50;">🌾 Crop Health Legend</h4>
     '''
    
    for category_name in ['healthy', 'moderate', 'unhealthy']:
        category_info = HEALTH_CATEGORIES[category_name]
        percentage = classification_results[category_name]['percentage']
        color = category_info['color']
        label = category_info['label']
        
        legend_html += f'''
     <div style="margin: 8px 0;">
         <i style="background:{color}; width:25px; height:25px; display:inline-block; border-radius:3px;"></i>
         <b>{label}</b>: {percentage:.1f}%
     </div>
     '''
    
    legend_html += f'''
     <hr style="margin: 10px 0;">
     <small>NDVI Range: {stats['min']:.3f} to {stats['max']:.3f}</small>
     </div>
     '''
    
    result_map.get_root().html.add_child(folium.Element(legend_html))
    
    folium.LayerControl().add_to(result_map)
    
    return result_map


def create_ndvi_histogram(ndvi_map):
    """
    Create NDVI distribution histogram
    
    Args:
        ndvi_map: 2D NumPy array of NDVI values
        
    Returns:
        Matplotlib figure
    """
    valid_ndvi = ndvi_map[~np.isnan(ndvi_map)]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Custom vibrant styling
    n, bins, patches = ax.hist(valid_ndvi, bins=50, color='#66BB6A', alpha=0.9, edgecolor='white')
    
    # Threshold lines with cleaner look
    ax.axvline(HEALTH_CATEGORIES['unhealthy']['threshold'][1], 
               color='#FF5252', linestyle='--', linewidth=2.5, label='Unhealthy Threshold')
    ax.axvline(HEALTH_CATEGORIES['moderate']['threshold'][1], 
               color='#FFC107', linestyle='--', linewidth=2.5, label='Healthy Threshold')
    
    # Clean up grid and spines
    ax.set_title('Vegetation Health Distribution (NDVI)', fontsize=14, fontweight='bold', pad=20, color='#333333')
    ax.set_xlabel('NDVI Value', fontsize=12, labelpad=10)
    ax.set_ylabel('Pixel Count', fontsize=12, labelpad=10)
    ax.legend(loc='upper left', frameon=True, framealpha=0.9)
    ax.grid(True, axis='y', alpha=0.2, linestyle='-')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Background color
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    return fig


def create_health_pie_chart(classification_results):
    """
    Create pie chart of health distribution
    
    Args:
        classification_results: Dict from classify_health()
        
    Returns:
        Matplotlib figure
    """
    labels = []
    sizes = []
    colors = []
    explode = []
    
    # Calculate max percentage safely for explode logic
    all_percentages = [classification_results[cat]['percentage'] for cat in ['healthy', 'moderate', 'unhealthy']]
    max_percentage = max(all_percentages) if all_percentages else 0

    for category_name in ['healthy', 'moderate', 'unhealthy']:
        category_info = HEALTH_CATEGORIES[category_name]
        percentage = classification_results[category_name]['percentage']
        
        if percentage > 0:
            labels.append(category_info['label'])
            sizes.append(percentage)
            colors.append(category_info['color'])
            # Explode the largest slice slightly for effect
            explode.append(0.05 if percentage == max_percentage else 0)
    
    # Donut chart style
    fig, ax = plt.subplots(figsize=(8, 8))
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
           startangle=90, pctdistance=0.85, explode=explode,
           textprops={'fontsize': 12, 'weight': 'bold', 'color': '#333333'})
           
    # Draw circle for donut effect
    centre_circle = plt.Circle((0,0), 0.70, fc='#f8f9fa')
    fig.gca().add_artist(centre_circle)
    
    # Style styling
    for text in texts:
        text.set_weight('bold')
    
    ax.set_title('Health Distribution', fontsize=16, fontweight='bold', pad=20, color='#333333')
    
    # Background color
    fig.patch.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    return fig
