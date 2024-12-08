from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

class ForecastParameters(BaseModel):
    horizon: int
    recent_months: Optional[int] = 3
    method: str = "moving_average"
    
    @validator('horizon')
    def validate_horizon(cls, v):
        if v <= 0:
            raise ValueError("Horizon must be positive")
        if v > 365:
            raise ValueError("Horizon cannot exceed 365 days")
        return v
    
    @validator('method')
    def validate_method(cls, v):
        valid_methods = ["moving_average", "exponential_smoothing", "arima"]
        if v not in valid_methods:
            raise ValueError(f"Method must be one of {valid_methods}")
        return v

class ForecastResult(BaseModel):
    forecast: List[float]
    method: str
    horizon: int
    timestamp: datetime = datetime.now()