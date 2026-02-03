"""
CropGuard - Satellite-Based Crop Health Monitoring System
Main Streamlit Application
"""
import streamlit as st
import json
import datetime
import numpy as np
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# Import utilities
from utils.satellite import (
    create_config,
    create_bbox_from_center,
    create_bbox_from_geojson,
    fetch_satellite_data,
    get_bbox_info
)
from utils.ndvi import compute_ndvi, classify_health
from utils.visualization import (
    create_base_map,
    create_result_map,
    create_ndvi_histogram,
    create_health_pie_chart
)
from config import APP_TITLE, APP_ICON, DEFAULT_LOCATION, DEFAULT_AREA_KM2

# Page configuration
st.set_page_config(
    page_title="CropGuard",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title(APP_TITLE)
st.markdown("**Automated crop health assessment using Sentinel-2 satellite imagery**")
st.markdown("---")

# Sidebar for credentials
with st.sidebar:
    st.header("🔐 Sentinel Hub Credentials")
    st.markdown("Get free credentials from [Sentinel Hub](https://www.sentinel-hub.com/)")
    
    client_id = st.text_input(
        "Client ID",
        type="password",
        help="Your Sentinel Hub OAuth Client ID"
    )
    
    client_secret = st.text_input(
        "Client Secret",
        type="password",
        help="Your Sentinel Hub OAuth Client Secret"
    )
    
    st.markdown("---")
    st.header("ℹ️ About")
    st.markdown("""
    **CropGuard** uses satellite data to monitor crop health via NDVI analysis.
    
    **Features:**
    - 📍 GPS location detection
    - 🔍 Global location search
    - ✏️ Interactive map drawing
    - 🛰️ Real Sentinel-2 data
    - 📊 Health classification
    """)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'ndvi_map' not in st.session_state:
    st.session_state.ndvi_map = None
if 'bbox' not in st.session_state:
    st.session_state.bbox = None
if 'classification_results' not in st.session_state:
    st.session_state.classification_results = None

# Main content
tab1, tab2 = st.tabs(["📍 Select Area", "📊 Results"])

with tab1:
    st.header("Step 1: Select Your Area of Interest")
    
    # Display interactive map
    st.subheader("🗺️ Interactive Map")
    st.markdown("""
    **Instructions:**
    1. 🎯 Click the location button (top-left) to find your current position
    2. 🔍 Use the search box (top-right) to find any location
    3. ✏️ Use drawing tools (left sidebar) to draw your field area
    4. **The area will be automatically detected!**
    """)
    
    # Create and display map
    map_obj = create_base_map()
    map_data = st_folium(map_obj, width=1200, height=600, key="main_map")
    
    # Auto-detect drawn area from map
    drawn_bbox = None
    if map_data and map_data.get('all_drawings'):
        try:
            # Get the last drawn shape
            drawings = map_data['all_drawings']
            if drawings:
                last_drawing = drawings[-1]
                geojson_data = last_drawing.get('geometry')
                
                if geojson_data:
                    drawn_bbox = create_bbox_from_geojson(geojson_data)
                    if drawn_bbox:
                        bbox_info = get_bbox_info(drawn_bbox)
                        st.success(f"✅ Area detected from map: ~{bbox_info['area_km2']:.2f} km²")
                        st.info(f"📍 Center: ({bbox_info['center_lat']:.4f}, {bbox_info['center_lon']:.4f})")
        except Exception as e:
            st.warning(f"Could not auto-detect drawn area: {str(e)}")
    
    st.markdown("---")
    
    # Input options
    st.header("Step 2: Provide Area Coordinates (Optional)")
    st.markdown("*If you drew on the map above, you can skip this and go directly to Step 3*")
    
    input_method = st.radio(
        "Or choose manual input method:",
        ["📍 Manual Coordinates", "🔍 Search Location"],
        horizontal=True
    )
    
    # Initialize manual bbox in session state
    if 'manual_bbox' not in st.session_state:
        st.session_state.manual_bbox = None
    
    # Use drawn bbox if available, otherwise use manual bbox
    bbox = drawn_bbox if drawn_bbox else st.session_state.manual_bbox
    
    if input_method == "📍 Manual Coordinates":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            lat = st.number_input(
                "Latitude",
                value=30.9010,
                format="%.4f",
                help="Center latitude of your area"
            )
        
        with col2:
            lon = st.number_input(
                "Longitude",
                value=75.8573,
                format="%.4f",
                help="Center longitude of your area"
            )
        
        with col3:
            area = st.number_input(
                "Area (km²)",
                value=DEFAULT_AREA_KM2,
                min_value=0.1,
                max_value=100.0,
                format="%.1f",
                help="Approximate area size"
            )
        
        if st.button("✅ Confirm Coordinates", type="primary"):
            st.session_state.manual_bbox = create_bbox_from_center(lat, lon, area)
            bbox = st.session_state.manual_bbox
            st.success(f"✅ Area selected: {area} km² around ({lat:.4f}, {lon:.4f})")
    
    elif input_method == "🔍 Search Location":
        location_query = st.text_input(
            "Enter location name or address",
            placeholder="e.g., Punjab, India or 30.9010, 75.8573"
        )
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            area = st.number_input(
                "Area (km²)",
                value=DEFAULT_AREA_KM2,
                min_value=0.1,
                max_value=100.0,
                format="%.1f"
            )
        
        if st.button("🔍 Search & Confirm", type="primary"):
            if location_query:
                try:
                    with st.spinner("Searching location..."):
                        geolocator = Nominatim(user_agent="cropguard")
                        location = geolocator.geocode(location_query)
                        
                        if location:
                            st.session_state.manual_bbox = create_bbox_from_center(
                                location.latitude,
                                location.longitude,
                                area
                            )
                            bbox = st.session_state.manual_bbox
                            st.success(f"✅ Found: {location.address}")
                            st.info(f"Coordinates: {location.latitude:.4f}, {location.longitude:.4f}")
                        else:
                            st.error("❌ Location not found. Try different search terms.")
                except Exception as e:
                    st.error(f"❌ Search error: {str(e)}")
            else:
                st.warning("⚠️ Please enter a location to search")
    
    # Show current selection status
    if bbox:
        bbox_info = get_bbox_info(bbox)
        if drawn_bbox:
            st.info(f"📍 **Active Selection**: Drawn area (~{bbox_info['area_km2']:.2f} km²)")
        else:
            st.info(f"📍 **Active Selection**: Manual input (~{bbox_info['area_km2']:.2f} km²)")
    
    st.markdown("---")
    
    # Analysis button
    st.header("Step 3: Run Analysis")
    
    if st.button("🚀 Analyze Crop Health", type="primary", use_container_width=True):
        # Validate inputs
        if not client_id or not client_secret:
            st.error("❌ Please enter Sentinel Hub credentials in the sidebar")
        elif not bbox:
            st.error("❌ Please select an area using one of the input methods above")
        else:
            # Create config
            config = create_config(client_id, client_secret)
            
            if not config:
                st.error("❌ Invalid credentials. Please check your Client ID and Secret.")
            else:
                try:
                    # Show progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Step 1: Fetch data
                    status_text.text("📡 Fetching satellite data...")
                    progress_bar.progress(20)
                    
                    bbox_info = get_bbox_info(bbox)
                    st.info(f"📍 Analyzing area: {bbox_info['area_km2']:.2f} km² around ({bbox_info['center_lat']:.4f}, {bbox_info['center_lon']:.4f})")
                    
                    data = fetch_satellite_data(config, bbox)
                    
                    if data is None:
                        st.error("❌ No satellite data found for this location/time period. Try a different area or time.")
                        progress_bar.empty()
                        status_text.empty()
                    else:
                        progress_bar.progress(50)
                        st.success(f"✅ Data fetched: {data.shape[0]} satellite images")
                        
                        # Step 2: Compute NDVI
                        status_text.text("🧮 Computing NDVI...")
                        progress_bar.progress(70)
                        
                        ndvi_map = compute_ndvi(data)
                        
                        if np.isnan(ndvi_map).all():
                            st.error("❌ Area was 100% cloudy. No valid NDVI data available.")
                            progress_bar.empty()
                            status_text.empty()
                        else:
                            progress_bar.progress(85)
                            
                            # Step 3: Classify
                            status_text.text("📊 Classifying crop health...")
                            classification_results = classify_health(ndvi_map)
                            
                            progress_bar.progress(100)
                            status_text.text("✅ Analysis complete!")
                            
                            # Store in session state
                            st.session_state.ndvi_map = ndvi_map
                            st.session_state.bbox = bbox
                            st.session_state.classification_results = classification_results
                            st.session_state.analysis_complete = True
                            
                            st.success("✅ Analysis complete! Check the **Results** tab.")
                            
                            # Clear progress indicators
                            import time
                            time.sleep(1)
                            progress_bar.empty()
                            status_text.empty()
                
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
                    import traceback
                    with st.expander("Show error details"):
                        st.code(traceback.format_exc())

with tab2:
    st.header("📊 Analysis Results")
    
    if not st.session_state.analysis_complete:
        st.info("👈 Please complete the analysis in the **Select Area** tab first.")
    else:
        ndvi_map = st.session_state.ndvi_map
        bbox = st.session_state.bbox
        classification_results = st.session_state.classification_results
        
        # Display statistics
        st.subheader("📈 Health Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🟢 Healthy",
                f"{classification_results['healthy']['percentage']:.1f}%",
                f"{classification_results['healthy']['count']:,} pixels"
            )
        
        with col2:
            st.metric(
                "🟡 Moderate",
                f"{classification_results['moderate']['percentage']:.1f}%",
                f"{classification_results['moderate']['count']:,} pixels"
            )
        
        with col3:
            st.metric(
                "🔴 Unhealthy",
                f"{classification_results['unhealthy']['percentage']:.1f}%",
                f"{classification_results['unhealthy']['count']:,} pixels"
            )
        
        with col4:
            stats = classification_results['statistics']
            st.metric(
                "📊 Mean NDVI",
                f"{stats['mean']:.3f}",
                f"Range: {stats['min']:.2f} - {stats['max']:.2f}"
            )
        
        st.markdown("---")
        
        # Display charts
        st.subheader("📊 Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**NDVI Distribution**")
            fig_hist = create_ndvi_histogram(ndvi_map)
            st.pyplot(fig_hist)
        
        with col2:
            st.markdown("**Health Distribution**")
            fig_pie = create_health_pie_chart(classification_results)
            st.pyplot(fig_pie)
        
        st.markdown("---")
        
        # Display result map
        st.subheader("🗺️ Interactive Result Map")
        st.markdown("Toggle between Map/Satellite view to see the NDVI overlay")
        
        result_map = create_result_map(ndvi_map, bbox, classification_results)
        st_folium(result_map, width=1200, height=600)
        
        st.markdown("---")
        
        # Detailed statistics table
        with st.expander("📋 Detailed Statistics"):
            stats = classification_results['statistics']
            
            st.markdown("**NDVI Statistics:**")
            stats_data = {
                "Metric": ["Mean", "Median", "Std Dev", "Min", "Max"],
                "Value": [
                    f"{stats['mean']:.4f}",
                    f"{stats['median']:.4f}",
                    f"{stats['std']:.4f}",
                    f"{stats['min']:.4f}",
                    f"{stats['max']:.4f}"
                ]
            }
            st.table(stats_data)
            
            st.markdown("**Health Classification:**")
            health_data = {
                "Category": ["Healthy (≥0.5)", "Moderate (0.2-0.5)", "Unhealthy (<0.2)"],
                "Pixels": [
                    f"{classification_results['healthy']['count']:,}",
                    f"{classification_results['moderate']['count']:,}",
                    f"{classification_results['unhealthy']['count']:,}"
                ],
                "Percentage": [
                    f"{classification_results['healthy']['percentage']:.2f}%",
                    f"{classification_results['moderate']['percentage']:.2f}%",
                    f"{classification_results['unhealthy']['percentage']:.2f}%"
                ]
            }
            st.table(health_data)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🌾 CropGuard - Powered by Sentinel-2 satellite imagery</p>
    <p>Data source: <a href='https://www.copernicus.eu/'>Copernicus Sentinel-2</a> (ESA)</p>
</div>
""", unsafe_allow_html=True)
