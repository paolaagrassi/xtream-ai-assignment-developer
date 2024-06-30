import logging
import pickle
import pandas as pd
import statistics

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
from src.utils.helpers import validate_data_has_no_zero_values

logger = logging.getLogger(__name__)


def create_dataframe_from_diamond_schema_for_prediction(
    data: DiamondFeaturesForPredictionSchema,
) -> pd.DataFrame:
    """
    Creates a dataframe for diamond price prediction from received data.

    Parameters
    ----------
    data: (DiamondFeaturesForPredictionSchema)
        The schema with the necessary columns to create the dataframe.

    Returns
    -------
    DataFrame
    """

    return pd.DataFrame(
        {
            DiamondColumnsEnum.CARAT.value: [data.carat],
            DiamondColumnsEnum.CUT.value: [data.cut],
            DiamondColumnsEnum.COLOR.value: [data.color],
            DiamondColumnsEnum.CLARITY.value: [data.clarity],
            DiamondColumnsEnum.DEPTH.value: [data.depth],
            DiamondColumnsEnum.TABLE.value: [data.table],
            DiamondColumnsEnum.PRICE.value: [0],
            DiamondColumnsEnum.X.value: [data.x],
            DiamondColumnsEnum.Y.value: [data.y],
            DiamondColumnsEnum.Z.value: [data.z],
        }
    )


def prepare_diamond_df_for_xgboost_model(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares the dataframe for xgboost model, converting the features into
    ordinal categorical data types and dropping the price column.

    Parameters
    ----------
    df: (DataFrame)
        The diamonds dataframe to be prepared.

    Returns
    -------
    df: (DataFrame)
        The diamonds dataframe preprocessed.

    Raises
    ------
    (ValueError, TypeError, KeyError):
        Raises if there are errors during the preprocessing process.
    """
    try:
        cut_categories_list = [cut.value for cut in DiamondCutEnum]
        df[DiamondColumnsEnum.CUT.value] = (
            dataset_service.convert_column_into_ordinal_categorical_data_type(
                df=df,
                column_name="cut",
                categories_list=cut_categories_list,
            )
        )

        color_categories_list = [color.value for color in DiamondColorEnum]
        df[DiamondColumnsEnum.COLOR.value] = (
            dataset_service.convert_column_into_ordinal_categorical_data_type(
                df=df,
                column_name="color",
                categories_list=color_categories_list,
            )
        )

        clarity_categories_list = [clarity.value for clarity in DiamondClarityEnum]
        df[DiamondColumnsEnum.CLARITY.value] = (
            dataset_service.convert_column_into_ordinal_categorical_data_type(
                df=df,
                column_name="clarity",
                categories_list=clarity_categories_list,
            )
        )

        df = df.drop(columns=DiamondColumnsEnum.PRICE.value)

        return df
    except (ValueError, TypeError, KeyError) as e:
        logger.error(f"Error while preparing dataframe. [Details]: {e}")
        raise e


def predict_diamond_price(data: DiamondFeaturesForPredictionSchema) -> str:
    """
    Receives the data with the values of the diamond to have price predicted
    and returns a string with the predicted price.

    Parameters
    ----------
    data: (DiamondFeaturesForPredictionSchema)
        Data of the diamond.

    Returns
    -------
    response: (str)
        A string with the price predicted.

    Raises
    ------
    (ValueError, TypeError, pickle.UnpicklingError, FileNotFoundError):
        Raises if some error occurs during preparing of dataframe or unpickling the model.
    """
    try:
        validate_data_has_no_zero_values(data)
        diamond_df: pd.DataFrame = create_dataframe_from_diamond_schema_for_prediction(
            data
        )
        model: XGBRegressor = model_service.load_pickle_model(
            path="data/models/model_xcgboost.pkl"
        )

        new_diamond_df = diamond_df.copy()
        new_diamond_df = prepare_diamond_df_for_xgboost_model(new_diamond_df)

        prediction = model_service.predict(df=new_diamond_df, model=model)
        response = f"The predicted value for the diamond is: ${prediction[0]}"

        return response
    except (ValueError, TypeError, pickle.UnpicklingError, FileNotFoundError) as e:
        logger.error(f"Error trying to predic diamond price. [Details]: {e}")
        raise e


def filter_diamonds_df_by_features(
    df: pd.DataFrame, features: DiamondFeaturesForSearchSchema
) -> pd.DataFrame:
    """
    Filter the diamonds df values with the same features (cut, color, clarity).

    Parameters
    ----------
    df: (DataFrame)
        The diamonds dataframe.
    features: (DiamondFeaturesForSearchSchema)
        Data with the features values.

    Returns
    -------
    DataFrame:
        Returns the diamonds dataframe with the filtered values.

    Raises
    ------
    ValueError:
        Raises if the filter found no diamonds.
    """
    new_df = df[
        (df[DiamondColumnsEnum.CLARITY.value] == features.clarity)
        & (df[DiamondColumnsEnum.COLOR.value] == features.color)
        & (df[DiamondColumnsEnum.CUT.value] == features.cut)
    ]
    if new_df.empty:
        raise ValueError("It was not found diamonds for the chosen features.")
    
    return new_df


def diamonds_df_filtered_by_similar_weight(
    df: pd.DataFrame, weight: float
) -> pd.DataFrame:
    """
    Filter the diamonds dataframe by similar weight.

    Parameters
    ----------
    df: (DataFrame)
        The diamonds dataframe to be filtered.
    weight: (float)
        The weight to be compared.

    Returns
    -------
    (DataFrame)
        Returns a dataframe with the results of the filtered values.
    """
    weight_average: float = statistics.mean(df["carat"])
    similar_weight_limit: float = weight_average - weight
    filtered_diamonds: list[pd.DataFrame] = []

    for carat in df[DiamondColumnsEnum.CARAT.value]:
        if abs((carat - weight)) <= similar_weight_limit:
            filtered_diamonds.append(df[df["carat"] == carat])

    return pd.concat(filtered_diamonds)


def search_diamond_by_features_and_similar_weight(
    data: DiamondFeaturesForSearchSchema,
) -> list[dict]:
    """
    Search in the diamonds csv for values with the same features (cut, color, clarity)
    and similar weight (carat).

    Parameters
    ----------
    data: (DiamondFeaturesForSearchSchema)
        Schema with the expected features values to search.

    Returns
    list_of_dataframes_as_dict: (list[dict])
        Returns a list of dicts of the found diamonds.

    Raises
    ------
    ValueError:
        Raises when the received carat's value is zero or there is no result for the applied filter.

    """
    try:
        validate_data_has_no_zero_values(data)

        df = dataset_service.create_dataframe_from_csv("data/diamonds.csv")

        filtered_df = filter_diamonds_df_by_features(df=df, features=data)
        filtered_df = diamonds_df_filtered_by_similar_weight(
            df=filtered_df, weight=data.carat
        )

        list_of_dataframes_as_dict = filtered_df.to_dict("records")

        return list_of_dataframes_as_dict

    except ValueError as e:
        logger.error(f"Error trying to search diamond. [Details]: {e}")
        raise e
