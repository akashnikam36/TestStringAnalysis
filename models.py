from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any

class StringAnalysisRequest(BaseModel):
    text : str = Field(description="The text string to analyze", min_length=1)

    @field_validator("text")
    def text_must_not_be_only_whitespacses(cls,v):
        if not v.strip():
            raise ValueError('Text cannot be empty or contain only whitespace')
        return v

class StringAnalysisResponse(BaseModel):
    input_text: str = Field(
        description="The original text that was analyzed"
    )
    analyses: Dict[str, Any] = Field(
        description="Dictionary containing the results of all requested analyses"
    ) 

class UserRegister(BaseModel):
    """
    Model for user registration request.
    Contains username and password for creating a new account.
    """
    username: str = Field(min_length=3, max_length=50, description="Username (3-50 characters)")
    password: str = Field(min_length=2, description="Password (minimum 2 characters)")


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")


class UserResponse(BaseModel):
    id: int = Field(description="User ID")
    username: str = Field(description="Username")
    
    class Config:
        # This allows Pydantic to work with SQLAlchemy models
        from_attributes = True
