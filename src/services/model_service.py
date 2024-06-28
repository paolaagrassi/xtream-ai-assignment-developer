import pandas as pd
import pickle
from xgboost.sklearn import XGBRegressor

def load_pickle_model(path: str):
    with open(path, 'rb') as f:
      model = pickle.load(f)
      return model
    
def predict(df: pd.DataFrame, model: XGBRegressor):
   prediction = model.predict(df)
   return prediction