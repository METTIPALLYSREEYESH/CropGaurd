"""
Analysis API Endpoints
Handles crop health analysis requests
"""
from fastapi import APIRouter, HTTPException
from models.schemas import AnalysisRequest, AnalysisResponse
import sys
import os
import numpy as np
import datetime

# Add parent directory to import utils from main project
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.satellite import create_config, fetch_satellite_data
from utils.ndvi import compute_ndvi, classify_health
from utils.ai_risk_model import calculate_ndvi_change, assess_risk, calculate_ai_score, get_risk_explanation, get_action_recommendation
from utils.crop_detection import detect_crop
from utils.confidence import calculate_confidence

router = APIRouter()

@router.post("/run", response_model=AnalysisResponse)
async def run_analysis(request: AnalysisRequest):
    """
    Run complete crop health analysis
    
    Returns NDVI data, classification, and AI risk assessment
    """
    try:
        # Create Sentinel Hub config
        config = create_config(request.client_id, request.client_secret)
        if not config:
            raise HTTPException(status_code=400, detail="Invalid Sentinel Hub credentials")
        
        # Create BBox object
        from sentinelhub import BBox, CRS
        bbox = BBox(
            [request.bbox.min_x, request.bbox.min_y, request.bbox.max_x, request.bbox.max_y],
            crs=CRS.WGS84
        )
        
        # Fetch satellite data for recent period
        end_date = datetime.datetime.now()
        start_date_recent = end_date - datetime.timedelta(days=7)
        time_interval_recent = (
            start_date_recent.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        
        data_recent = fetch_satellite_data(config, bbox, time_interval_recent)
        
        if data_recent is None or len(data_recent) == 0:
            raise HTTPException(status_code=400, detail="No satellite data available for this location/time")
        
        # Compute NDVI for recent period
        ndvi_recent = compute_ndvi(data_recent)
        
        # Fetch data for past period (for comparison)
        start_date_past = end_date - datetime.timedelta(days=21)
        end_date_past = end_date - datetime.timedelta(days=14)
        time_interval_past = (
            start_date_past.strftime('%Y-%m-%d'),
            end_date_past.strftime('%Y-%m-%d')
        )
        
        data_past = fetch_satellite_data(config, bbox, time_interval_past)
        ndvi_past = compute_ndvi(data_past) if data_past is not None and len(data_past) > 0 else ndvi_recent
        
        # Classify NDVI
        classification_results = classify_health(ndvi_recent)
        
        if classification_results is None:
            raise HTTPException(status_code=400, detail="Failed to classify NDVI data")
        
        # Add color information to classification
        from config import HEALTH_CATEGORIES
        classification_results['healthy']['color'] = HEALTH_CATEGORIES['healthy']['color']
        classification_results['moderate']['color'] = HEALTH_CATEGORIES['moderate']['color']
        classification_results['unhealthy']['color'] = HEALTH_CATEGORIES['unhealthy']['color']
        
        # Calculate NDVI change
        ndvi_change = calculate_ndvi_change(ndvi_recent, ndvi_past)
        
        # Assess risk
        risk_level = assess_risk(ndvi_change, classification_results)
        
        # Calculate AI score
        ai_score = calculate_ai_score(classification_results, ndvi_change)
        
        # Detect crop
        detected_crop, crop_confidence = detect_crop(
            ndvi_recent,
            (request.bbox.min_y + request.bbox.max_y) / 2,
            (request.bbox.min_x + request.bbox.max_x) / 2
        )
        
        # Calculate confidence
        confidence = calculate_confidence(ndvi_recent, cloud_cover_pct=0)
        
        # Get explanations
        risk_explanation = get_risk_explanation(risk_level, ndvi_change, lang='en')
        action_recommendation = get_action_recommendation(risk_level, lang='en')
        
        # Prepare response
        ai_results = {
            "risk_level": risk_level,
            "ai_score": ai_score,
            "ndvi_change": float(ndvi_change),
            "confidence": confidence,
            "risk_explanation": risk_explanation,
            "action_recommendation": action_recommendation,
            "detected_crop": detected_crop,
            "crop_confidence": crop_confidence
        }
        
        bbox_info = {
            "center_lat": (request.bbox.min_y + request.bbox.max_y) / 2,
            "center_lon": (request.bbox.min_x + request.bbox.max_x) / 2,
            "area_km2": request.area_km2
        }
        
        # Convert numpy arrays to lists
        ndvi_map_list = ndvi_recent.tolist()
        
        return {
            "ndvi_map": ndvi_map_list,
            "classification": classification_results,
            "ai_results": ai_results,
            "bbox_info": bbox_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
