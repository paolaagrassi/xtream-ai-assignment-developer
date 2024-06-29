import pandas as pd
import logging


logger = logging.getLogger(__name__)

def convert_column_into_ordinal_categorical_data_type(
    df: pd.DataFrame, column_name: str, categories_list: list[str]
) -> pd.Categorical:
    """
    Converts a column in a pandas DataFrame into an ordinal categorical data type.

    Parameters
    ----------
    df: (pd.DataFrame)
        The pandas DataFrame containing the column to convert.
    column_name: (str) 
        The name of the column to convert into a categorical data type.
    categories_list: (list[str])
        A list of strings defining the valid categories and their order.

    Returns
    -------
    Categorical: 
        The converted column as an ordinal categorical data type.

    Raises
    -------
    KeyError:
        Raises if the data being converted to Categorical contains 
    values that are not present in the categories argument.

    ValueError:
        Raises if there is invalid categories, incompatible data type or invalid order.

    TypeError:
        Raises if there is invalid data type for comparison or the operation is unsupported.
    
    """

    try:
        return pd.Categorical(df[column_name], categories=categories_list, ordered=True)
    
    except (ValueError, TypeError, KeyError) as e:
        logger.error(f"Error converting column '{column_name}' to categorical. [Details]: {e}")
        raise e

def create_dataframe_from_csv(path: str) -> pd.DataFrame:
    """
    Creates a dataframe from received csv path.

    Parameters
    ----------
    path: (str)
        The CSV's path.

    Returns
    -------
    (DataFrame)
        The generated dataframe.    

    Raises
    ------
    FileNotFoundError
        Raises when the CSV's path is not found.
    """
    try:
        return pd.read_csv(path)
    except FileNotFoundError as e:
        logger.error(f"Error converting csv from path {path} to dataframe. [Details]: {e}")
        raise e