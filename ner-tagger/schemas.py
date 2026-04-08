from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class AnalysisRequest(BaseModel):
    """
    Standard input for NLP analysis.
    """
    text: str = Field(
        ...,
        min_length=1,
        max_length=50000,
        description="The input text to analyze."
    )
    language: Optional[str] = Field(
        None,
        description="Explicit language override (e.g., 'en', 'es')."
    )

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be purely whitespace")
        return v


class TokenFeature(BaseModel):
    """
    Detailed token-level analysis.
    """
    model_config = ConfigDict(populate_by_name=True)

    text: str = Field(..., alias="Text")
    lemma: str = Field(..., alias="Morpheme/Stem")
    pos: str = Field(..., alias="POS")
    tag: str = Field(..., alias="Tag")
    dependency: str = Field(..., alias="Dependency")


class EntityResult(BaseModel):
    """
    Grouped entities by category.
    """
    model_config = ConfigDict(populate_by_name=True)

    person: List[str] = Field(default_factory=list, alias="Person")
    organisation: List[str] = Field(default_factory=list, alias="Organisation")
    location: List[str] = Field(default_factory=list, alias="Location")
    date: List[str] = Field(default_factory=list, alias="Date")
    other: List[str] = Field(default_factory=list, alias="Other")


class AnalysisResponse(BaseModel):
    """
    Universal NLP API response.
    """
    model_config = ConfigDict(protected_namespaces=())

    entities: EntityResult
    tokens: List[TokenFeature]
    detected_language: str
    status: str = "success"
    model_used: str


class HealthStatus(BaseModel):
    """
    Service health metadata.
    """
    model_config = ConfigDict(protected_namespaces=())

    status: str = "healthy"
    version: str = "2.0.0"
    model_loaded: bool
