import pandas as pd
from src.schemas.diamond_schema import DiamondSchema
from src.services import dataset_service, model_service
from xgboost.sklearn import XGBRegressor

def create_dataframe_from_diamond_schema(schema_values: DiamondSchema) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "carat": [schema_values.carat],
            "cut": [schema_values.cut],
            "color": [schema_values.color],
            "clarity": [schema_values.clarity],
            "depth": [schema_values.depth],
            "table": [schema_values.table],
            "price": [0],
            "x": [schema_values.x],
            "y": [schema_values.y],
            "z": [schema_values.z],
        }
    )


def prepare_diamond_df(df: pd.DataFrame) -> pd.DataFrame:
    cut_categories_list = ["Fair", "Good", "Very Good", "Ideal", "Premium"]
    df["cut"] = dataset_service.convert_column_into_ordinal_categorical_data_type(
        df=df,
        column_name="cut",
        categories_list=cut_categories_list,
    )

    color_categories_list = ["D", "E", "F", "G", "H", "I", "J"]
    df["color"] = dataset_service.convert_column_into_ordinal_categorical_data_type(
        df=df,
        column_name="color",
        categories_list=color_categories_list,
    )

    clarity_categories_list = ["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I1"]
    df["clarity"] = dataset_service.convert_column_into_ordinal_categorical_data_type(
        df=df,
        column_name="clarity",
        categories_list=clarity_categories_list,
    )

    df = df.drop(columns="price")

    return df

def predict_diamond_price(diamond_data: DiamondSchema):
    diamond_df: pd.DataFrame = create_dataframe_from_diamond_schema(
        diamond_data
    )
    model: XGBRegressor = model_service.load_pickle_model(
        path="/home/paolaagrassi/xtream-code/xtream-ai-assignment-developer/data/models/model_xcgboost.pkl"
    )

    new_diamond_df = diamond_df.copy()
    new_diamond_df = prepare_diamond_df(new_diamond_df)

    prediction = model_service.predict(df=new_diamond_df, model=model)
    response = f"The predicted value for the diamond is: ${prediction[0]}"

    return response