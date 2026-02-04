"""
Field Management API Endpoints
Save, load, and manage field locations
"""
from fastapi import APIRouter, HTTPException
from models.schemas import SaveFieldRequest, FieldInfo
from typing import List
import sys
import os

# Add parent directory to import utils from main project
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.field_manager import save_field, load_fields, delete_field, get_field_bbox

router = APIRouter()

@router.get("/", response_model=List[FieldInfo])
async def get_all_fields():
    """
    Get all saved fields
    
    Returns list of saved field information
    """
    try:
        fields_dict = load_fields()
        
        # Convert to list of FieldInfo
        fields_list = []
        for name, data in fields_dict.items():
            fields_list.append({
                "name": name,
                "bbox": data['bbox'],
                "last_analysis": data['last_analysis']
            })
        
        return fields_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load fields: {str(e)}")

@router.post("/")
async def create_field(request: SaveFieldRequest):
    """
    Save a new field
    
    Stores field location and last analysis results
    """
    try:
        # Create a simple bbox object for save_field
        class SimpleBBox:
            def __init__(self, min_x, min_y, max_x, max_y):
                self.min_x = min_x
                self.min_y = min_y
                self.max_x = max_x
                self.max_y = max_y
        
        bbox = SimpleBBox(
            request.bbox.min_x,
            request.bbox.min_y,
            request.bbox.max_x,
            request.bbox.max_y
        )
        
        # Convert AIResults to dict
        ai_results_dict = request.ai_results.dict()
        
        success = save_field(
            request.name,
            bbox,
            ai_results_dict,
            request.detected_crop
        )
        
        if success:
            return {"message": f"Field '{request.name}' saved successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to save field")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save field: {str(e)}")

@router.delete("/{field_name}")
async def remove_field(field_name: str):
    """
    Delete a saved field
    """
    try:
        success = delete_field(field_name)
        
        if success:
            return {"message": f"Field '{field_name}' deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Field '{field_name}' not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete field: {str(e)}")

@router.get("/{field_name}/bbox")
async def get_field_coordinates(field_name: str):
    """
    Get bbox coordinates for a specific field
    """
    try:
        bbox = get_field_bbox(field_name)
        
        if bbox:
            return {"bbox": bbox}
        else:
            raise HTTPException(status_code=404, detail=f"Field '{field_name}' not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get field bbox: {str(e)}")
