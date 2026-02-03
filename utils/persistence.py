"""
Persistence handling for CropGuard.
Saves and loads analysis results to/from local disk.
"""
import os
import json
import numpy as np
import streamlit as st
from sentinelhub import BBox, CRS

DATA_DIR = "data"
METADATA_FILE = os.path.join(DATA_DIR, "last_analysis.json")
NDVI_RECENT_FILE = os.path.join(DATA_DIR, "ndvi_recent.npy")
NDVI_PAST_FILE = os.path.join(DATA_DIR, "ndvi_past.npy")

def ensure_data_dir():
    """Ensure data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_analysis(bbox, classification_results, ai_results, ndvi_map_recent, ndvi_map_past=None):
    """
    Save current analysis to disk.
    """
    try:
        ensure_data_dir()
        
        # Prepare metadata
        # Convert BBox to list for JSON serialization
        bbox_list = [bbox.min_x, bbox.min_y, bbox.max_x, bbox.max_y]
        
        metadata = {
            "bbox": bbox_list,
            "crs": str(bbox.crs),
            "classification_results": classification_results,
            "ai_results": ai_results,
            "has_past_data": ndvi_map_past is not None,
            "timestamp": str(np.datetime64('now'))
        }
        
        # Save metadata
        with open(METADATA_FILE, 'w') as f:
            json.dump(metadata, f, indent=4)
            
        # Save NumPy arrays
        np.save(NDVI_RECENT_FILE, ndvi_map_recent)
        
        if ndvi_map_past is not None:
            np.save(NDVI_PAST_FILE, ndvi_map_past)
        else:
            # If persists from previous run but now is None, delete old file to avoid confusion
            if os.path.exists(NDVI_PAST_FILE):
                os.remove(NDVI_PAST_FILE)
                
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def load_last_analysis():
    """
    Load last analysis from disk into session state.
    Returns True if successful, False otherwise.
    """
    try:
        if not os.path.exists(METADATA_FILE) or not os.path.exists(NDVI_RECENT_FILE):
            return False
            
        # Load metadata
        with open(METADATA_FILE, 'r') as f:
            metadata = json.load(f)
            
        # Reconstruct BBox
        bbox_coords = metadata['bbox']
        # CRS handling is simplified here assuming WGS84 for now, or parsing the string could be more complex
        # But our app mostly uses WGS84
        bbox = BBox(bbox=bbox_coords, crs=CRS.WGS84)
        
        # Load NumPy arrays
        ndvi_map_recent = np.load(NDVI_RECENT_FILE)
        
        ndvi_map_past = None
        if metadata.get('has_past_data') and os.path.exists(NDVI_PAST_FILE):
            ndvi_map_past = np.load(NDVI_PAST_FILE)
            
        # Populate session state
        st.session_state.bbox = bbox
        st.session_state.classification_results = metadata['classification_results']
        st.session_state.ai_results = metadata['ai_results']
        st.session_state.ndvi_map = ndvi_map_recent
        st.session_state.ndvi_map_past = ndvi_map_past
        st.session_state.analysis_complete = True
        
        return True
    except Exception as e:
        print(f"Error loading data: {e}")
        return False
