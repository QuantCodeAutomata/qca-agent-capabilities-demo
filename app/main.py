"""FastAPI microservice main application."""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime
from app.models import (
    HealthResponse,
    AnalysisRequest,
    AnalysisResponse,
    ReportResponse,
    ErrorResponse
)
from app.storage import data_store

app = FastAPI(
    title="Analysis Microservice",
    description="A FastAPI microservice for data analysis and reporting",
    version="1.0.0"
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unexpected errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "detail": str(exc)}
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    description="Returns the current health status of the service"
)
async def health_check():
    """
    Health check endpoint to verify service is running.
    
    Returns:
        HealthResponse with status and timestamp
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow()
    )


@app.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Analyze data endpoint",
    description="Accepts JSON data for analysis and stores it"
)
async def analyze_data(request: AnalysisRequest):
    """
    Accept and store data for analysis.
    
    Args:
        request: AnalysisRequest containing data and optional metadata
        
    Returns:
        AnalysisResponse with analysis details
        
    Raises:
        HTTPException: If data validation fails or storage error occurs
    """
    try:
        if not request.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data field cannot be empty"
            )
        
        record = data_store.create_record(
            data=request.data,
            metadata=request.metadata
        )
        
        return AnalysisResponse(
            id=record.id,
            status="success",
            message="Data analyzed and stored successfully",
            timestamp=record.timestamp
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process analysis: {str(e)}"
        )


@app.get(
    "/report",
    response_model=ReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Get analysis report",
    description="Returns all stored analysis data"
)
async def get_report():
    """
    Retrieve all stored analysis records.
    
    Returns:
        ReportResponse containing all analysis records
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        records = data_store.get_all_records()
        
        return ReportResponse(
            total_records=len(records),
            records=records
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve report: {str(e)}"
        )


@app.get(
    "/",
    summary="Root endpoint",
    description="Welcome message and API information"
)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Analysis Microservice API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze (POST)",
            "report": "/report",
            "docs": "/docs"
        }
    }
