import pandas as pd
import logging


logger = logging.getLogger(__name__)

def convert_column_into_ordinal_categorical_data_type(
    df: pd.DataFrame, column_name: str, categories_list: list[str]
) -> pd.Categorical:
    try:
        return pd.Categorical(df[column_name], categories=categories_list, ordered=True)
    except (ValueError, TypeError, KeyError) as e:
        logger.error(f"Error converting column '{column_name}' to categorical. [Details]: {e}")
        raise e

