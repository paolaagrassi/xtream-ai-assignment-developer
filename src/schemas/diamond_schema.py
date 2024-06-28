from typing import Optional
from pydantic import BaseModel
from src.utils.enums.diamonds_enums import DiamondClarityEnum, DiamondColorEnum, DiamondCutEnum


class BaseDiamondSchema(BaseModel):
    carat: float
    cut: DiamondCutEnum
    color: DiamondColorEnum
    clarity: DiamondClarityEnum
    

class DiamondFeaturesForPredictionSchema(BaseDiamondSchema):
    depth: float
    table: float
    x: float
    y: float
    z: float


class DiamondFeaturesForSearchSchema(BaseDiamondSchema):
    pass