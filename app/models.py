"""Pydantic models for request and response validation."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Current timestamp")


class AnalysisRequest(BaseModel):
    """Request model for analysis endpoint."""
    data: Dict[str, Any] = Field(..., description="Data to be analyzed")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "data": {"temperature": 23.5, "humidity": 60},
                "metadata": {"source": "sensor-1", "location": "room-A"}
            }
        }


class AnalysisResponse(BaseModel):
    """Response model for analysis endpoint."""
    id: str = Field(..., description="Unique analysis ID")
    status: str = Field(..., description="Analysis status")
    message: str = Field(..., description="Status message")
    timestamp: datetime = Field(..., description="Analysis timestamp")


class AnalysisRecord(BaseModel):
    """Model for stored analysis records."""
    id: str = Field(..., description="Unique analysis ID")
    data: Dict[str, Any] = Field(..., description="Analyzed data")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadata")
    timestamp: datetime = Field(..., description="Analysis timestamp")
    status: str = Field(..., description="Analysis status")


class ReportResponse(BaseModel):
    """Response model for report endpoint."""
    total_records: int = Field(..., description="Total number of records")
    records: List[AnalysisRecord] = Field(..., description="List of analysis records")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
