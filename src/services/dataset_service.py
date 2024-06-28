import pandas as pd

def convert_column_into_ordinal_categorical_data_type(
    df: pd.DataFrame, column_name: str, categories_list: list[str]
) -> pd.Categorical:
    return pd.Categorical(df[column_name], categories=categories_list, ordered=True)

