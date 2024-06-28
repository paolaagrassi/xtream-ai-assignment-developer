from typing import Optional
from pydantic import BaseModel



class BaseDiamondSchema(BaseModel):
    carat: float
    cut: str
    color: str
    clarity: str
    

class DiamondFeaturesForPredictionSchema(BaseDiamondSchema):
    depth: float
    table: float
    x: float
    y: float
    z: float


class DiamondFeaturesForSearchSchema(BaseDiamondSchema):
    pass