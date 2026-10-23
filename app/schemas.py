from pydantic import BaseModel, ConfigDict, Field

class PredictionInput(BaseModel):
    model_config = ConfigDict(strict=True)
    age: int = Field(ge=18, le=100)
    systolic: int = Field(ge=70, le=250)
    diastolic: int = Field(ge=40, le=150)
    glucose: float = Field(gt=0, le=500)
    bmi: float = Field(gt=10, le=70)

class PredictionResponse(BaseModel):
    predicted_class: int
    probability_class_1: float
    model_version: str
