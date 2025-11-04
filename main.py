from fastapi import FastAPI, HTTPException, Query, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from sqlalchemy.orm import Session
import logging

from string_operations import StringAnalyzer
from models import StringAnalysisRequest, StringAnalysisResponse, UserRegister, UserLogin, Token, UserResponse
from config import Settings
from database import engine, get_db
from db_models import Base, User
from auth import (
    hash_password, authenticate_user, create_access_token, get_current_user
)
settings = Settings()

Base.metadata.create_all(bind=engine)

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
    current_user: User = Depends(get_current_user),
    analyses: Optional[List[str]] = Query(
        default=None,
        description = "Specific analyses to perform  Options: word_count, char_count"
    ),
    
):
    logger.info(f" Received analysis request for text of length {len(request.text)} from {current_user.username}")
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


@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    logger.info(f"Registration attempt for username: {user_data.username}")
    
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        logger.warning(f"Registration failed: username '{user_data.username}' already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered. Please choose a different username."
        )
    
    hashed_password = hash_password(user_data.password)
    
    # Create new user
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"User registered successfully: {user_data.username}")
    return new_user


@app.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for username: {user_data.username}")
    
    # Authenticate user
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        logger.warning(f"Login failed for username: {user_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    
    logger.info(f"User logged in successfully: {user_data.username}")
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)