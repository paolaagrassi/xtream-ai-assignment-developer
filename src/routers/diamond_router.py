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
    """
    Predicts the price of the diamond.

    Cut options: "Fair","Good","Very Good","Ideal","Premium"

    Color options: "D","E","F","G","H","I","J"

    Clarity options: "IF","VVS1","VVS2","VS1","VS2","SI1","SI2","I1"
    """
    try:
        return diamond_service.predict_diamond_price(data=body)
    except (
        ValueError,
        TypeError,
        KeyError,
        pickle.UnpicklingError,
        FileNotFoundError,
    ) as e:
        raise HTTPException(status_code=400, detail=(str(e)))


@router.post("/search")
def post_search_diamond_by_features_and_similar_weight(body: DiamondFeaturesForSearchSchema):
    """
    Returns a list of diamonds filtered by features and similar weight.

    Cut options: "Fair","Good","Very Good","Ideal","Premium"

    Color options: "D","E","F","G","H","I","J"
    
    Clarity options: "IF","VVS1","VVS2","VS1","VS2","SI1","SI2","I1"
    """
    try:
        return diamond_service.search_diamond_by_features_and_similar_weight(data=body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=(str(e)))
