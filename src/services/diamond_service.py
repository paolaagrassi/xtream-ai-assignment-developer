import logging
import pickle
import pandas as pd
import statistics

from pydantic import BaseModel
from xgboost.sklearn import XGBRegressor
from src.schemas.diamond_schema import (
    DiamondFeaturesForPredictionSchema,
    DiamondFeaturesForSearchSchema,
)
from src.services import dataset_service, model_service
from src.utils.enums.diamonds_enums import (
    DiamondClarityEnum,
    DiamondColorEnum,
    DiamondCutEnum,
    DiamondColumnsEnum,
)

logger = logging.getLogger(__name__)


def create_dataframe_from_diamond_schema(
    data: DiamondFeaturesForPredictionSchema,
) -> pd.DataFrame:
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
        df[DiamondColumnsEnum.CUT.value] = dataset_service.convert_column_into_ordinal_categorical_data_type(
            df=df,
            column_name="cut",
            categories_list=cut_categories_list,
        )

        color_categories_list = [color.value for color in DiamondColorEnum]
        df[DiamondColumnsEnum.COLOR.value] = dataset_service.convert_column_into_ordinal_categorical_data_type(
            df=df,
            column_name="color",
            categories_list=color_categories_list,
        )

        clarity_categories_list = [clarity.value for clarity in DiamondClarityEnum]
        df[DiamondColumnsEnum.CLARITY.value] = (
            dataset_service.convert_column_into_ordinal_categorical_data_type(
                df=df,
                column_name="clarity",
                categories_list=clarity_categories_list,
            )
        )

        df = df.drop(columns="price")

        return df
    except (ValueError, TypeError, KeyError) as e:
        logger.error(f"Error while preparing dataframe. [Details]: {e}")
        raise e


def validate_data_has_no_zero_values(data: BaseModel) -> None:
    for value in data:
        if 0 in value:
            raise ValueError(f"{value[0]} must have value grather than 0.")


def predict_diamond_price(data: DiamondFeaturesForPredictionSchema) -> str:
    try:
        validate_data_has_no_zero_values(data)
        diamond_df: pd.DataFrame = create_dataframe_from_diamond_schema(data)
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


def filter_diamonds_by_features(
    df: pd.DataFrame, features: DiamondFeaturesForSearchSchema
) -> pd.DataFrame:
    return df[
        (df[DiamondColumnsEnum.CLARITY.value] == features.clarity)
        & (df[DiamondColumnsEnum.COLOR.value] == features.color)
        & (df[DiamondColumnsEnum.CUT.value] == features.cut)
    ]


def diamonds_df_filtered_by_similar_weight(
    df: pd.DataFrame, weight: float
) -> pd.DataFrame:
    weight_average: float = statistics.mean(df["carat"])
    similar_weight_limit: float = weight_average - weight
    filtered_diamonds: list[pd.DataFrame] = []

    for carat in df[DiamondColumnsEnum.CARAT.value]:
        if abs((carat - weight)) <= similar_weight_limit:
            filtered_diamonds.append(df[df["carat"] == carat])

    return pd.concat(filtered_diamonds)


def search_diamond_by_features_and_similar_weight(data: DiamondFeaturesForSearchSchema) -> list[dict]:
    try:
        validate_data_has_no_zero_values(data)
        df = dataset_service.create_dataframe_from_csv("data/diamonds.csv")
        filtered_df = filter_diamonds_by_features(df=df, features=data)
        filtered_df = diamonds_df_filtered_by_similar_weight(
            df=filtered_df, weight=data.carat
        )

        list_of_dataframes_as_dict = filtered_df.to_dict('records')
        return list_of_dataframes_as_dict

    except ValueError as e:
        logger.error(f"Error trying to search diamond. [Details]: {e}")
        raise e
