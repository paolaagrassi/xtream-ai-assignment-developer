from src.services.dataset_service import create_dataframe_from_csv
import pandas as pd
import pytest

class TestDatasetService:

    class TestCreateDataframeFromCSV:

        def test_raises_error_when_path_is_not_fount(self):
            invalid_path = '../../data/no_csv.csv'
            with pytest.raises(FileNotFoundError) as e:
                create_dataframe_from_csv(invalid_path)
            
            assert isinstance(e, pytest.ExceptionInfo)
            assert "No such file or directory" == e.value.args[1]

        def test_returns_dataframe_when_passing_valid_csv_path(self):
            response = create_dataframe_from_csv('data/diamonds.csv')

            assert isinstance(response, pd.DataFrame)
