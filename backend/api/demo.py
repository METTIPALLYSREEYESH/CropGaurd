"""
Demo Mode API Endpoints
Provides pre-loaded demo scenarios
"""
from fastapi import APIRouter, HTTPException
from models.schemas import DemoResponse
import json
import os
import numpy as np

router = APIRouter()

@router.get("/scenario", response_model=DemoResponse)
async def get_demo_scenario():
    """
    Load pre-configured demo scenario
    
    Returns HIGH RISK demo data for instant presentation
    """
    try:
        # Load demo data
        demo_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "demo_scenario.json")
        
        with open(demo_file, 'r', encoding='utf-8') as f:
            demo_data = json.load(f)
        
        # Create synthetic NDVI map
        demo_ndvi = np.random.uniform(0.2, 0.6, (100, 100))
        demo_ndvi[demo_ndvi > 0.5] = np.nan
        
        # Prepare classification results
        classification = {
            'healthy': {
                'percentage': demo_data['classification']['healthy']['percentage'],
                'count': 1520,
                'color': '#4CAF50'
            },
            'moderate': {
                'percentage': demo_data['classification']['moderate']['percentage'],
                'count': 2850,
                'color': '#FFC107'
            },
            'unhealthy': {
                'percentage': demo_data['classification']['unhealthy']['percentage'],
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
        
        # Prepare AI results
        ai_results = {
            'risk_level': demo_data['risk_level'],
            'ai_score': demo_data['ai_score'],
            'ndvi_change': demo_data['ndvi_change'],
            'confidence': demo_data['confidence'],
            'risk_explanation': "⚠️ Significant vegetation decline detected. Severe water stress combined with high heat (34.5°C) and low humidity (32%). No rainfall for 15 days. Immediate irrigation required.",
            'action_recommendation': "🚨 **URGENT**: Increase irrigation immediately. Inspect field for heat stress damage. Consider emergency watering schedule.",
            'detected_crop': demo_data['detected_crop'],
            'crop_confidence': demo_data['crop_confidence']
        }
        
        return {
            "demo_data": demo_data,
            "ndvi_map": demo_ndvi.tolist(),
            "classification": classification,
            "ai_results": ai_results
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Demo scenario file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load demo: {str(e)}")
