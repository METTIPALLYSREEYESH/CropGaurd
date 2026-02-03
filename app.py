"""
CropGuard - Crop Health Monitoring Application
"""
import streamlit as st
import json
import os
import datetime
import numpy as np
from streamlit_folium import st_folium
import importlib

# Force reload of ai_risk_model to pick up latest changes
import utils.ai_risk_model
importlib.reload(utils.ai_risk_model)
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
from utils.ai_risk_model import (
    calculate_ndvi_change,
    assess_risk,
    get_risk_explanation,
    calculate_ai_score,
    get_action_recommendation
)
from utils.persistence import save_analysis, load_last_analysis
from utils.crop_detection import detect_crop
from utils.translations import get_text, TRANSLATIONS
from utils.report_generator import generate_pdf_report
from utils.field_manager import save_field, load_fields, get_field_bbox
from utils.confidence import calculate_confidence, get_confidence_color, get_confidence_icon
from config import APP_TITLE, APP_ICON, DEFAULT_LOCATION, DEFAULT_AREA_KM2

# Page configuration
st.set_page_config(
    page_title="CropGuard",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR UI POLISH ---
st.markdown("""
<style>
    /* Main Title */
    .css-10trblm h1 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #0d47a1;
    }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05); 
    }
    div[data-testid="stMetric"] label {
        color: #424242;
        font-weight: 500;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #1a237e;
        font-weight: bold;
    }
    
    /* Risk Card Styling */
    .risk-card {
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #fafafa;
    }
    
    /* Buttons */
    div.stButton > button {
        background-color: #29b6f6;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #0288d1;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Title - Get language first
lang = st.session_state.get('language', 'en')
st.title(get_text('app_title', lang))
st.markdown(f"**{get_text('app_subtitle', lang)}**")

# Initialize language in session state
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Sidebar
with st.sidebar:
    # Language Selector (must be first to set session state)
    lang_options = {
        'English': 'en',
        'हिंदी (Hindi)': 'hi',
        'తెలుగు (Telugu)': 'te'
    }
    selected_lang = st.selectbox(
        "🌐 Language / भाषा / భాష",
        options=list(lang_options.keys()),
        index=0
    )
    st.session_state.language = lang_options[selected_lang]
    lang = st.session_state.language
    
    # Farmer Mode Toggle
    st.markdown("---")
    if 'farmer_mode' not in st.session_state:
        st.session_state.farmer_mode = False
    
    farmer_mode = st.toggle("👨‍🌾 Farmer-Friendly Mode", value=st.session_state.farmer_mode,
                            help="Simple language without technical terms")
    st.session_state.farmer_mode = farmer_mode
    
    # Demo Mode Button
    st.markdown("---")
    demo_button = st.button("🎬 Load Demo Scenario", use_container_width=True, type="primary",
                            help="Click to load a pre-configured HIGH RISK scenario for demonstration")
    
    if demo_button:
        import json
        import os
        
        demo_file = "data/demo_scenario.json"
        
        # Check if file exists
        if not os.path.exists(demo_file):
            st.error(f"❌ Demo file not found: {demo_file}")
        else:
            try:
                with open(demo_file, 'r', encoding='utf-8') as f:
                    demo_data = json.load(f)
                
                # Set demo mode flags
                st.session_state.demo_mode = True
                st.session_state.demo_data = demo_data
                st.session_state.analysis_complete = False  # Reset to trigger demo load
                
                # Force rerun to show demo
                st.rerun()
                
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON in demo file: {str(e)}")
            except Exception as e:
                st.error(f"❌ Demo load failed: {str(e)}")
    
    # Saved Fields
    st.markdown("---")
    st.subheader("📁 Saved Fields")
    
    saved_fields = load_fields()
    if saved_fields:
        field_names = ["Select a field..."] + list(saved_fields.keys())
        selected_field = st.selectbox("Load Field:", field_names, key="field_selector")
        
        if selected_field != "Select a field...":
            bbox_data = get_field_bbox(selected_field)
            if bbox_data:
                st.info(f"📍 {selected_field} loaded")
                # Store in session for use
                st.session_state.loaded_field_bbox = bbox_data
    
    # Now use the selected language for headers
    st.markdown("---")
    st.header(f"📍 {get_text('sidebar_title', lang)}")
    
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
lang = st.session_state.get('language', 'en')
tab1, tab2 = st.tabs([f"📍 {get_text('select_area_tab', lang)}", f"📊 {get_text('results_tab', lang)}"])

with tab1:
    st.header(get_text('select_area_tab', lang))
    
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
                    
                    # --- Step 1: Recent Data (Last 10 days) ---
                    status_text.text("📡 Fetching RECENT satellite data (Last 10 days)...")
                    progress_bar.progress(10)
                    
                    bbox_info = get_bbox_info(bbox)
                    st.info(f"📍 Analyzing area: {bbox_info['area_km2']:.2f} km² around ({bbox_info['center_lat']:.4f}, {bbox_info['center_lon']:.4f})")
                    
                    # Date range for RECENT data
                    end_date = datetime.datetime.now()
                    start_date_recent = end_date - datetime.timedelta(days=10)
                    time_interval_recent = (
                        start_date_recent.strftime('%Y-%m-%d'),
                        end_date.strftime('%Y-%m-%d')
                    )
                    
                    data_recent = fetch_satellite_data(config, bbox, time_interval=time_interval_recent)
                    
                    # --- Step 2: Past Data (20-30 days ago) ---
                    # We need this for change detection
                    if data_recent is not None:
                        status_text.text("⏳ Fetching PAST satellite data (Baseline)...")
                        progress_bar.progress(30)
                        
                        start_date_past = end_date - datetime.timedelta(days=40) # Go back further to ensure overlap
                        end_date_past = end_date - datetime.timedelta(days=20)
                        time_interval_past = (
                            start_date_past.strftime('%Y-%m-%d'),
                            end_date_past.strftime('%Y-%m-%d')
                        )
                        data_past = fetch_satellite_data(config, bbox, time_interval=time_interval_past)
                    else:
                        data_past = None

                    
                    if data_recent is None:
                        st.error("❌ No satellite data found for the RECENT period. Try a different area or check cloud cover.")
                        progress_bar.empty()
                        status_text.empty()
                    else:
                        progress_bar.progress(50)
                        st.success(f"✅ Data fetched: {data_recent.shape[0]} recent scenes")
                        
                        # Step 3: Compute NDVI for Recent Data
                        status_text.text("🧮 Computing NDVI & AI Risk Analysis...")
                        progress_bar.progress(70)
                        
                        ndvi_map_recent = compute_ndvi(data_recent)
                        
                        if np.isnan(ndvi_map_recent).all():
                            st.error("❌ Area was 100% cloudy in recent pass. No valid analysis possible.")
                            progress_bar.empty()
                            status_text.empty()
                        else:
                            # Step 4: Compute NDVI for Past Data (if available)
                            ndvi_map_past = None
                            ndvi_change = 0.0
                            
                            if data_past is not None:
                                ndvi_map_past = compute_ndvi(data_past)
                                # If past data is totally cloudy, we can't do change detection properly
                                if np.isnan(ndvi_map_past).all():
                                    ndvi_map_past = None
                            
                            # --- AI MODEL EXECUTION ---
                            # 1. Calculate stats
                            valid_ndvi_recent = ndvi_map_recent[~np.isnan(ndvi_map_recent)]
                            current_mean = float(np.nanmean(valid_ndvi_recent)) if len(valid_ndvi_recent) > 0 else 0.0
                            
                            past_mean = 0.0
                            if ndvi_map_past is not None:
                                valid_ndvi_past = ndvi_map_past[~np.isnan(ndvi_map_past)]
                                past_mean = float(np.nanmean(valid_ndvi_past)) if len(valid_ndvi_past) > 0 else current_mean
                            
                            # 2. FEATURE 6: Crop Detection
                            current_month = datetime.datetime.now().month
                            detected_crop, crop_confidence = detect_crop(current_mean, current_month)

                            # 3. Compute Change & Risk
                            final_past_mean = past_mean if ndvi_map_past is not None else current_mean
                            ndvi_change = calculate_ndvi_change(current_mean, final_past_mean)
                            risk_level = assess_risk(ndvi_change)
                            # Pass language to XAI
                            current_lang = st.session_state.get('language', 'en')
                            risk_explanation = get_risk_explanation(risk_level, lang=current_lang)
                            action_recommendation = get_action_recommendation(risk_level, lang=current_lang)
                            ai_score = calculate_ai_score(risk_level, current_mean)
                            
                            
                            progress_bar.progress(85)
                            
                            # Step 5: Classify (Traditional)
                            status_text.text("📊 Finalizing classification...")
                            classification_results = classify_health(ndvi_map_recent)
                            
                            progress_bar.progress(100)
                            status_text.text("✅ Analysis complete!")
                            
                            # Store in session state
                            st.session_state.ndvi_map = ndvi_map_recent
                            st.session_state.ndvi_map_past = ndvi_map_past
                            st.session_state.bbox = bbox
                            st.session_state.classification_results = classification_results
                            
                            # Store AI Results
                            st.session_state.ai_results = {
                                'risk_level': risk_level,
                                'risk_explanation': risk_explanation,
                                'action_recommendation': action_recommendation,
                                'ai_score': ai_score,
                                'ndvi_change': ndvi_change,
                                'current_mean': current_mean,
                                'past_mean': final_past_mean,
                                'detected_crop': detected_crop,
                                'crop_confidence': crop_confidence
                            }
                            
                            st.session_state.analysis_complete = True
                            
                            # --- PERSISTENCE: SAVE DATA ---
                            if save_analysis(bbox, classification_results, st.session_state.ai_results, ndvi_map_recent, ndvi_map_past):
                                st.toast("💾 Analysis saved locally!", icon="✅")
                            
                            st.success(get_text('analysis_complete', current_lang))
                            
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
    lang = st.session_state.get('language', 'en')
    st.header(f"📊 {get_text('results_tab', lang)}")
    
    # --- DEMO MODE HANDLING ---
    if st.session_state.get('demo_mode', False):
        st.warning("🎬 **DEMO MODE ACTIVE** - Showing pre-loaded scenario", icon="🎭")
        demo_data = st.session_state.get('demo_data', {})
        
        # Create demo NDVI map (synthetic)
        import numpy as np
        demo_ndvi = np.random.uniform(0.2, 0.6, (100, 100))
        demo_ndvi[demo_ndvi > 0.5] = np.nan  # Add some gaps
        
        # Override session state with demo data
        st.session_state.ndvi_map = demo_ndvi
        st.session_state.classification_results = {
            'healthy': {
                'percentage': demo_data.get('classification', {}).get('healthy', {}).get('percentage', 15.2),
                'count': 1520,
                'color': '#4CAF50'
            },
            'moderate': {
                'percentage': demo_data.get('classification', {}).get('moderate', {}).get('percentage', 28.5),
                'count': 2850,
                'color': '#FFC107'
            },
            'unhealthy': {
                'percentage': demo_data.get('classification', {}).get('unhealthy', {}).get('percentage', 56.3),
                'count': 5630,
                'color': '#F44336'
            },
            'statistics': {
                'mean': 0.42,
                'std': 0.18,
                'min': 0.05,
                'max': 0.75
            }
        }
        st.session_state.ai_results = {
            'risk_level': demo_data.get('risk_level', 'High Risk'),
            'ai_score': demo_data.get('ai_score', 32),
            'ndvi_change': demo_data.get('ndvi_change', -0.26),
            'risk_explanation': "⚠️ Significant vegetation decline detected. Severe water stress combined with high heat (34.5°C) and low humidity (32%). No rainfall for 15 days. Immediate irrigation required.",
            'action_recommendation': "🚨 **URGENT**: Increase irrigation immediately. Inspect field for heat stress damage. Consider emergency watering schedule.",
            'detected_crop': demo_data.get('detected_crop', 'Rice'),
            'crop_confidence': demo_data.get('crop_confidence', 'High'),
            'confidence': demo_data.get('confidence', 'High')
        }
        st.session_state.analysis_complete = True
    
    # --- PERSISTENCE: LOAD DATA IF NEEDED ---
    if not st.session_state.analysis_complete:
        # Try to load from disk if not in session
        if load_last_analysis():
            st.toast("📂 Loaded previous analysis from disk.", icon="ℹ️")

    if not st.session_state.analysis_complete:
        st.info(get_text('no_analysis', lang))
    else:
        ndvi_map = st.session_state.ndvi_map
        bbox = st.session_state.get('bbox')
        classification_results = st.session_state.classification_results
        ai_results = st.session_state.get('ai_results', {})
        
        # --- FEATURE 1, 3, 4, 6, 7: INTEGRATED AI DASHBOARD ---
        if ai_results:
            risk_level = ai_results['risk_level']
            weather = ai_results.get('weather_context', {})
            detected_crop = ai_results.get('detected_crop', 'Unknown')
            
            risk_color = "#388e3c"  # Stable Green
            if risk_level == 'High Risk':
                risk_color = "#d32f2f"  # Alarm Red
            elif risk_level == 'Medium Risk':
                risk_color = "#f57c00"  # Warning Orange
                
            st.markdown(f"""
            <div style="padding: 20px; background-color: {risk_color}25; border-left: 5px solid {risk_color}; border-radius: 5px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="color: {risk_color}; margin: 0;">{ai_results['risk_level'].upper()}</h2>
                    <span style="background-color: white; padding: 5px 10px; border-radius: 15px; font-weight: bold; border: 1px solid #ccc;">🌾 {detected_crop} ({ai_results.get('crop_confidence', 'Low')} Conf.)</span>
                </div>
                <p style="font-size: 18px; margin: 15px 0;"><strong>🤖 AI Analysis:</strong> {ai_results['risk_explanation']}</p>
                <p style="font-size: 18px; margin: 10px 0; background-color: white; padding: 10px; border-radius: 5px; border: 1px solid {risk_color};"><strong>🚜 Action:</strong> {ai_results['action_recommendation']}</p>
                <hr style="border-top: 1px solid {risk_color}50;">
                <p style="margin: 0; font-size: 14px;">📉 <strong>NDVI Change:</strong> {ai_results['ndvi_change']:.3f}</p>
            </div>
            """, unsafe_allow_html=True)

        # --- FEATURE 2: AI HEALTH SCORE ---
        st.subheader(f"🧠 {get_text('ai_health_score', lang)}")
        score = ai_results.get('ai_score', 0)
        score_color = "#388e3c" if score > 79 else ("#f57c00" if score > 49 else "#d32f2f")
        
        # Flexbox centering + white-space: nowrap prevents line break
        st.markdown(f"""
        <div style="text-align: center; border: 4px solid {score_color}; border-radius: 50%; width: 150px; height: 150px; display: flex; align-items: center; justify-content: center; margin: 20px auto; box-shadow: 0 0 15px {score_color}40; background-color: white;">
            <span style="font-size: 38px; font-weight: bold; color: {score_color}; white-space: nowrap;">
                {score}<span style="font-size: 24px; color: #888;">/100</span>
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # --- AI CONFIDENCE SCORE ---
        confidence = ai_results.get('confidence')
        if not confidence:
            # Calculate confidence if not provided
            confidence = calculate_confidence(ndvi_map, cloud_cover_pct=0)
        
        conf_color = get_confidence_color(confidence)
        conf_icon = get_confidence_icon(confidence)
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: -10px; margin-bottom: 20px;">
            <span style="background-color: {conf_color}20; color: {conf_color}; padding: 8px 16px; border-radius: 20px; font-weight: bold; border: 2px solid {conf_color};">
                🎯 Confidence: {confidence} {conf_icon}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # --- PDF REPORT DOWNLOAD ---
        st.markdown("---")
        col_pdf, col_spacer = st.columns([1, 2])
        with col_pdf:
            if st.button(f"📄 {get_text('download_report', lang)}", use_container_width=True):
                with st.spinner(get_text('generating_report', lang)):
                    try:
                        # Get bbox info
                        bbox_info = {
                            'center_lat': (bbox.min_y + bbox.max_y) / 2,
                            'center_lon': (bbox.min_x + bbox.max_x) / 2,
                            'area_km2': st.session_state.get('area_km2', 1.0)
                        }
                        
                        # Generate PDF
                        pdf_bytes = generate_pdf_report(
                            ai_results,
                            bbox_info,
                            classification_results,
                            ndvi_map,
                            ai_results.get('detected_crop', 'Unknown'),
                            lang=lang  # Pass current language
                        )
                        
                        # Download button
                        st.download_button(
                            label="⬇️ Click to Download PDF",
                            data=pdf_bytes,
                            file_name=f"CropGuard_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.success("✅ Report generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")

        st.markdown("---")

        # --- FEATURE 5: TIME COMPARISON MODE ---
        st.subheader(f"🗺️ {get_text('interactive_maps', lang)}")
        
        map_option = st.radio(
            get_text('select_map_view', lang),
            [get_text('recent_analysis', lang), get_text('time_comparison', lang)],
            horizontal=True
        )
        
        if map_option == get_text('recent_analysis', lang):
             st.markdown(get_text('toggle_map_view', lang))
             result_map = create_result_map(ndvi_map, bbox, classification_results)
             st_folium(result_map, width=1200, height=600)
             
        else: # Time Comparison Mode
            st.markdown("**Left: 30 Days Ago (Baseline) | Right: Recent (Current)**")
            if st.session_state.get('ndvi_map_past') is not None:
                # We reuse result map logic but display two columns
                col_past, col_recent = st.columns(2)
                ndvi_map_past = st.session_state.ndvi_map_past
                
                # Simple classification for past map just for viz
                results_past = classify_health(ndvi_map_past) 
                
                with col_past:
                     st.caption("📅 Past (Baseline)")
                     map_past = create_result_map(ndvi_map_past, bbox, results_past)
                     st_folium(map_past, width=550, height=400, key="map_past")
                     
                with col_recent:
                     st.caption("📅 Recent (Current)")
                     map_recent = create_result_map(ndvi_map, bbox, classification_results)
                     st_folium(map_recent, width=550, height=400, key="map_recent")
            else:
                 st.warning("⚠️ Historical data unavailable for this specific region (likely cloud cover). Comparison mode disabled.")
        
        st.markdown("---")
        
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
        
        # --- SAVE CURRENT FIELD ---
        if not st.session_state.get('demo_mode', False) and bbox:
            st.markdown("---")
            col_save1, col_save2 = st.columns([2, 1])
            with col_save1:
                field_name = st.text_input("Field Name:", placeholder="e.g., North Rice Field", key="save_field_name")
            with col_save2:
                st.write("")  # Spacer
                st.write("")  # Spacer
                if st.button("💾 Save This Field", use_container_width=True, disabled=not field_name):
                    if field_name:
                        try:
                            save_field(field_name, bbox, ai_results, ai_results.get('detected_crop', 'Unknown'))
                            st.success(f"✅ Field '{field_name}' saved successfully!")
                        except Exception as e:
                            st.error(f"Error saving field: {str(e)}")
        
        # --- WHY THIS MATTERS SECTION ---
        st.markdown("---")
        st.markdown("### 💡 Why This Matters")
        
        col_why1, col_why2 = st.columns(2)
        with col_why1:
            st.markdown("""
            **🌱 Early Detection**  
            Catch crop stress before visible damage occurs. Satellite data reveals health issues 7-14 days earlier than the human eye.
            
            **🛰️ Zero Hardware**  
            No expensive IoT sensors needed. Works anywhere with satellite coverage - 100% satellite-based monitoring.
            """)
        
        with col_why2:
            st.markdown("""
            **🌍 Global Scale**  
            Monitor from 1 acre to 1 million acres instantly. Perfect for small farmers and large agricultural operations.
            
            **👨‍🌾 Farmer First**  
            Simple, actionable advice (e.g., "Irrigate now"). No PhD required to understand crop health status.
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🌾 CropGuard - Powered by Sentinel-2 satellite imagery</p>
    <p>Data source: <a href='https://www.copernicus.eu/'>Copernicus Sentinel-2</a> (ESA)</p>
</div>
""", unsafe_allow_html=True)
