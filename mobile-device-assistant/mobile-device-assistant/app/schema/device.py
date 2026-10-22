from pydantic import BaseModel, Field, field_validator
from typing import Literal, Dict, Annotated, List

class Device (BaseModel):
    brand: str = Field(description = "Device Brand")
    model: str = Field(description = "Device Model")
    specs: Dict[str,str] = Field(description = "Device Specs")
    release_year: int = Field (ge= 1973, le=2026, description = "Device Release Year")
    price_tier: Annotated[Literal["budget","mid-range","flagship"], Field(description="Device Price Tier")]
    
    
    @field_validator("brand")
    @classmethod
    def brand_validator (cls,v):
        if not v.strip():
            raise ValueError ("Device Brand can't be empty or only whitespace")
        return v.strip()

    @field_validator("model")
    @classmethod
    def model_validator (cls,v):
        if not v.strip():
            raise ValueError ("Device Model can't be empty or only whitespace")
        return v.strip()
    
    @field_validator("specs")
    @classmethod
    def specs_validator (cls,v):
        for key,value in v.items():
            if not key.strip() or not value.strip():
                raise ValueError ("Device Specs can't have empty or only whitespace Spec.")
        return {k.strip(): v.strip() for k, v in v.items()}
    
    @field_validator("price_tier", mode="before")
    @classmethod
    def price_tier_validator (cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        raise ValueError ("Trice tier have to be a string.")
    
    
    
    
    
    
    
    

class ExtractRequest (BaseModel):
    text:str = Field (max_length=500,description="Input for specification extraction")
    @field_validator("text")
    @classmethod
    def text_validator (cls,v):
        if not v.strip():
            raise ValueError ("Input can't be empty or only whitespace")
        return v.strip()

    
    
class ExtractResponse (Device):
    pass
    
    
class SearchRequest (BaseModel):
    q:str = Field (max_length=500, description="Search Query")
    
    @field_validator("q")
    @classmethod
    def q_validator (cls,v):
        if not v.strip():
            raise ValueError ("Search Query can't be empty or only whitespace")
        return v.strip()    
    
    
class SearchResult (BaseModel):
    document:str = Field (description="Retrived Document")
    score: float = Field (description="Document Score")

    @field_validator("document")
    @classmethod
    def document_validator (cls,v):
        if not v.strip():
            raise ValueError ("Document can't be empty or only whitespace")
        return v.strip()   
    
        
class SearchResponse (BaseModel):
    results: List[SearchResult]