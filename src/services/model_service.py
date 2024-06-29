import logging
import pandas as pd
import pickle
from xgboost.sklearn import XGBRegressor


logger = logging.getLogger(__name__)


def load_pickle_model(path: str) -> any:
    """
    Loads a pickled model from the received file path.

    Parameters
    ----------
    path: (str) 
        The file path of the pickle file containing the model.

    Returns
    -------
    model: (Any)
        The loaded model object.
    
    Raises
    ------
    FileNotFoundError:
        Raises if the file path doesn't exist.
    pickle.UnpicklingError:
        Raises if there is an error during the unpickling process.
    """
    try:
        with open(path, "rb") as f:
            model = pickle.load(f)
            return model
    except (pickle.UnpicklingError, FileNotFoundError) as e:
        logger.error(f"Error unpickling model. [Details]: {e}")
        raise e


def predict(df: pd.DataFrame, model: XGBRegressor) -> list:
    """
    Makes predictions using a fitted XGBRegressor model.

    This function takes a pandas DataFrame containing features and a fitted XGBRegressor model
    as input. It then utilizes the model to predict the target variable for each data point
    in the DataFrame. The predicted values are returned as a list.

    Parameters:
    -----------
    df: (pd.DataFrame)
        The DataFrame containing the features for prediction and the same columns as the data used to fit the model.
    model: (XGBRegressor)
        A fitted XGBRegressor model object, previously trained on data with compatible features.

    Returns:
    --------
    list:
        A list containing the predicted target values for each data point in the DataFrame.

    Raises:
    ValueError:
        Raises if the columns don't match the feature names used to train the model, or invalid input shape.
    TypeError:
        Raises if the model is not a valid XCGBoost model or if the input DataFrame is not a valid data type.
    """

    try:
        prediction = model.predict(df)
        return prediction
    except (ValueError, TypeError) as e:
        logger.error(f"Error during prediction. [Details]: {e}")
        raise e
