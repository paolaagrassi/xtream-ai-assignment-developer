import logging
import pickle
import pandas as pd
from xgboost.sklearn import XGBRegressor
from src.schemas.diamond_schema import DiamondFeaturesForPredictionSchema
from src.services import dataset_service, model_service
from src.utils.enums.diamonds_enums import DiamondClarityEnum, DiamondColorEnum, DiamondCutEnum

logger = logging.getLogger(__name__)

def create_dataframe_from_diamond_schema(data: DiamondFeaturesForPredictionSchema) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "carat": [data.carat],
            "cut": [data.cut],
            "color": [data.color],
            "clarity": [data.clarity],
            "depth": [data.depth],
            "table": [data.table],
            "price": [0],
            "x": [data.x],
            "y": [data.y],
            "z": [data.z],
        }
    )


def prepare_diamond_df(df: pd.DataFrame) -> pd.DataFrame:
    try:
        cut_categories_list = [cut.value for cut in DiamondCutEnum]
        df["cut"] = dataset_service.convert_column_into_ordinal_categorical_data_type(
            df=df,
            column_name="cut",
            categories_list=cut_categories_list,
        )

        color_categories_list = [color.value for color in DiamondColorEnum]
        df["color"] = dataset_service.convert_column_into_ordinal_categorical_data_type(
            df=df,
            column_name="color",
            categories_list=color_categories_list,
        )

        clarity_categories_list = [clarity.value for clarity in DiamondClarityEnum]
        df["clarity"] = dataset_service.convert_column_into_ordinal_categorical_data_type(
            df=df,
            column_name="clarity",
            categories_list=clarity_categories_list,
        )

        df = df.drop(columns="price")

        return df
    except (ValueError, TypeError, KeyError) as e:
        logger.error(f"Error while preparing dataframe. [Details]: {e}")
        raise e

def validate_data_to_predict_diamond(data: DiamondFeaturesForPredictionSchema) -> None:
    for value in data:
        if 0 in value:
            raise ValueError(f'{value[0]} must have value grather than 0.')


def predict_diamond_price(data: DiamondFeaturesForPredictionSchema) -> str:
    try:
        validate_data_to_predict_diamond(data)
        diamond_df: pd.DataFrame = create_dataframe_from_diamond_schema(
            data
    )
        model: XGBRegressor = model_service.load_pickle_model(
            path="data/models/model_xcgboost.pkl"
        )

        new_diamond_df = diamond_df.copy()
        new_diamond_df = prepare_diamond_df(new_diamond_df)

        prediction = model_service.predict(df=new_diamond_df, model=model)
        response = f"The predicted value for the diamond is: ${prediction[0]}"

        return response
    except (ValueError, TypeError, pickle.UnpicklingError, AttributeError) as e:
        logger.error(f"Error trying to predic diamond price. [Details]: {e}")
        raise e
