import logging
import pandas as pd
import pickle
from xgboost.sklearn import XGBRegressor


logger = logging.getLogger(__name__)


def load_pickle_model(path: str):
    try:
        with open(path, "rb") as f:
            model = pickle.load(f)
            return model
    except (pickle.UnpicklingError, AttributeError) as e:
        logger.error(f"Error unpickling model. [Details]: {e}")
        raise e


def predict(df: pd.DataFrame, model: XGBRegressor) -> list:
    try:
        prediction = model.predict(df)
        return prediction
    except (ValueError, TypeError) as e:
        logger.error(f"Error during prediction. [Details]: {e}")
        raise e
