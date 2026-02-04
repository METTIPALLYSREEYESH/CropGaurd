"""
Pydantic models for request/response schemas
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class BBox(BaseModel):
    """Bounding box coordinates"""
    min_x: float = Field(..., description="Minimum longitude")
    min_y: float = Field(..., description="Minimum latitude")
    max_x: float = Field(..., description="Maximum longitude")
    max_y: float = Field(..., description="Maximum latitude")

class AnalysisRequest(BaseModel):
    """Request for crop analysis"""
    bbox: BBox
    area_km2: float = Field(1.0, gt=0, description="Field area in square kilometers")
    client_id: str = Field(..., description="Sentinel Hub client ID")
    client_secret: str = Field(..., description="Sentinel Hub client secret")

class HealthCategory(BaseModel):
    """Health classification category"""
    percentage: float
    count: int
    color: str

class ClassificationResults(BaseModel):
    """NDVI classification results"""
    healthy: HealthCategory
    moderate: HealthCategory
    unhealthy: HealthCategory
    statistics: Dict[str, float]

class AIResults(BaseModel):
    """AI risk assessment results"""
    risk_level: str
    ai_score: int
    ndvi_change: float
    confidence: str
    risk_explanation: str
    action_recommendation: str
    detected_crop: str
    crop_confidence: str

class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    ndvi_map: List[List[float]]
    classification: ClassificationResults
    ai_results: AIResults
    bbox_info: Dict[str, float]

class SaveFieldRequest(BaseModel):
    """Request to save a field"""
    name: str
    bbox: BBox
    ai_results: AIResults
    detected_crop: str

class FieldInfo(BaseModel):
    """Saved field information"""
    name: str
    bbox: BBox
    last_analysis: Dict[str, Any]

class PDFRequest(BaseModel):
    """Request to generate PDF report"""
    ai_results: AIResults
    bbox_info: Dict[str, float]
    classification: ClassificationResults
    ndvi_map: List[List[float]]
    detected_crop: str
    language: str = "en"

class DemoResponse(BaseModel):
    """Demo scenario response"""
    demo_data: Dict[str, Any]
    ndvi_map: List[List[float]]
    classification: ClassificationResults
    ai_results: AIResults
