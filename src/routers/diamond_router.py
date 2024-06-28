from fastapi import APIRouter

from src.schemas.diamond_schema import DiamondSchema
from src.services import diamond_service

router = APIRouter(prefix="/diamond")

@router.post("/predict-price")
def post_predicted_diamond_price(body: DiamondSchema):
    return diamond_service.predict_diamond_price(diamond_data=body)
