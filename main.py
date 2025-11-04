from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from sqlalchemy.orm import Session
import logging

from string_operations import StringAnalyzer
from models import StringAnalysisRequest, StringAnalysisResponse
from config import Settings

settings = Settings()

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins= settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


analyzer = StringAnalyzer()

@app.get("/")
async def root():
    """
    Root endpoint - provides basic API information
    """
    return {
        "service": "String Analysis API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and container orchestration
    """
    return {
        "status": "healthy",
        "max_input_size": settings.MAX_INPUT_SIZE
    }

@app.post("/analyze", response_model=StringAnalysisResponse)
async def analyze_string(
    request: StringAnalysisRequest,
    analyses: Optional[List[str]] = Query(
        default=None,
        description = "Specific analyses to perform  Options: word_count, char_count"
    ),
):
    logger.info(f" Received analysis request for text of length {len(request.text)}")
    if len(request.text) > settings.MAX_INPUT_SIZE:
        logger.warning(f"Input size exceeded: {len(request.text)} > {settings.MAX_INPUT_SIZE}")
        raise HTTPException(
            status_code=413,
            detail=f"Input text exceeds maximum allowed size of {settings.MAX_INPUT_SIZE} characters"
        )
    
    # Check for empty input
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Input text cannot be empty or contain only whitespace"
        )
    
    try:
        result = analyzer.analyze(request.text, analyses)
        logger.info(f"Successfully completed analysis with {len(result.analyses)} metrics")
        return result
    except ValueError as ve:
        # Handle invalid analysis type requests
        logger.error(f"Invalid analysis request: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"Unexpected error during analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during analysis. Please try again."
        )

@app.get("/available-analyses")
async def get_available_analyses():
    return {
        "available_analyses": list(analyzer.get_available_analyses().keys()),
        "descriptions": analyzer.get_available_analyses()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)