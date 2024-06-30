from sqlalchemy.orm import Session

from src.models.api_request_model import APIrequestModel
from src.schemas.api_requests_schema import ApiRequestsSchema


def save_api_requests_to_database(db: Session, request_data: ApiRequestsSchema) -> None:
    """
    Saves API request data to the database.

    Parameters
    ----------
    db: (Session)
        An SQLAlchemy Session object used to interact with the database.
    request_data: (ApiRequestsSchema) 
        An instance of the `ApiRequestsSchema` class containing the API request data to be saved.
    
    Returns
    -------
    None
    """
    
    return APIrequestModel(
        request_type=request_data.request_type,
        path=request_data.path,
        created_at=request_data.created_at,
        response=request_data.response,
        status_code=request_data.status_code,
    ).save(db)
