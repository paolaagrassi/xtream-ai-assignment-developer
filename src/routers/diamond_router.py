from datetime import datetime
import pickle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.database_config import get_db
from src.models.api_request_model import APIrequestModel
from src.schemas.api_requests_schema import ApiRequestsSchema
from src.schemas.diamond_schema import (
    DiamondFeaturesForPredictionSchema,
    DiamondFeaturesForSearchSchema,
)
from src.services import diamond_service
from src.services.api_requests_service import save_api_requests_to_database

router = APIRouter(prefix="/diamond")


@router.post("/predict-price")
def post_predicted_diamond_price(
    body: DiamondFeaturesForPredictionSchema, db: Session = Depends(get_db)
):
    """
    Predicts the price of the diamond.

    Cut options: "Fair","Good","Very Good","Ideal","Premium"

    Color options: "D","E","F","G","H","I","J"

    Clarity options: "IF","VVS1","VVS2","VS1","VS2","SI1","SI2","I1"
    """
    try:
        response = diamond_service.predict_diamond_price(data=body)
        if response:
            request_data = ApiRequestsSchema(
                request_type="post",
                path="/diamond/predict-price",
                response=response,
                status_code=200,
                created_at=datetime.now(),
            )
            save_api_requests_to_database(request_data=request_data, db=db)
        return response
    except (
        ValueError,
        TypeError,
        KeyError,
        pickle.UnpicklingError,
        FileNotFoundError,
    ) as e:
        request_data = ApiRequestsSchema(
            request_type="post",
            path="/diamond/predict-price",
            response=str(e),
            status_code=400,
            created_at=datetime.now(),
        )
        save_api_requests_to_database(request_data=request_data, db=db)
        raise HTTPException(status_code=400, detail=(str(e)))


@router.post("/search")
def post_search_diamond_by_features_and_similar_weight(
    body: DiamondFeaturesForSearchSchema,
    db: Session = Depends(get_db)
):
    """
    Returns a list of diamonds filtered by features and similar weight.

    Cut options: "Fair","Good","Very Good","Ideal","Premium"

    Color options: "D","E","F","G","H","I","J"

    Clarity options: "IF","VVS1","VVS2","VS1","VS2","SI1","SI2","I1"
    """
    try:
        response = diamond_service.search_diamond_by_features_and_similar_weight(data=body)
        if response:
            request_data = ApiRequestsSchema(
                request_type="post",
                path="/diamond/search",
                response=str(response),
                status_code=200,
                created_at=datetime.now(),
            )
            save_api_requests_to_database(request_data=request_data, db=db)
        return response
    except ValueError as e:
        request_data = ApiRequestsSchema(
            request_type="post",
            path="/diamond/search",
            response=str(e),
            status_code=400,
            created_at=datetime.now(),
        )
        raise HTTPException(status_code=400, detail=(str(e)))
