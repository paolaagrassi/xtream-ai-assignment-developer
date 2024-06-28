import pickle
from fastapi import APIRouter, HTTPException

from src.schemas.diamond_schema import (
    DiamondFeaturesForPredictionSchema,
    DiamondFeaturesForSearchSchema,
)
from src.services import diamond_service

router = APIRouter(prefix="/diamond")


@router.post("/predict-price")
def post_predicted_diamond_price(body: DiamondFeaturesForPredictionSchema):
    try:
        return diamond_service.predict_diamond_price(data=body)
    except (
        ValueError,
        TypeError,
        KeyError,
        pickle.UnpicklingError,
        AttributeError,
    ) as e:
        raise HTTPException(status_code=400, detail=(str(e)))


@router.post("/search")
def post_search_diamond_by_features_and_similar_weight(body: DiamondFeaturesForSearchSchema):
    try:
        return diamond_service.search_diamond_by_features_and_similar_weight(data=body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=(str(e)))
