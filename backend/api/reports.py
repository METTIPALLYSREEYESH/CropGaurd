"""
Report Generation API Endpoints
Generate and download PDF reports
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from models.schemas import PDFRequest
import sys
import os
import numpy as np

# Add parent directory to import utils from main project
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.report_generator import generate_pdf_report

router = APIRouter()

@router.post("/generate")
async def generate_report(request: PDFRequest):
    """
    Generate PDF report
    
    Returns PDF file as binary response
    """
    try:
        # Convert ndvi_map list back to numpy array
        ndvi_map = np.array(request.ndvi_map)
        
        # Convert Pydantic models to dicts
        ai_results_dict = request.ai_results.dict()
        classification_dict = request.classification.dict()
        
        # Generate PDF
        pdf_bytes = generate_pdf_report(
            ai_results_dict,
            request.bbox_info,
            classification_dict,
            ndvi_map,
            request.detected_crop,
            lang=request.language
        )
        
        # Return as downloadable PDF
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=CropGuard_Report.pdf"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")
