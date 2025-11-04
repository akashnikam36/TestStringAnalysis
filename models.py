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
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
