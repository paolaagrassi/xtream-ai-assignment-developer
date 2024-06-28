import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from src.schemas.diamond_schema import DiamondFeaturesForSearchSchema
from src.services.diamond_service import (
    filter_diamonds_by_features,
    diamonds_df_filtered_by_similar_weight,
)
from src.utils.enums.diamonds_enums import (
    DiamondClarityEnum,
    DiamondColorEnum,
    DiamondCutEnum,
    DiamondColumnsEnum
)


class TestDiamondService:

    @pytest.fixture
    def df_result_after_filter(self):
        data = {
            DiamondColumnsEnum.CARAT.value: [
                1.1,
                0.83,
                1.03,
                0.78,
            ],
            DiamondColumnsEnum.CLARITY.value: [
                DiamondClarityEnum.si2.value,
                DiamondClarityEnum.si2.value,
                DiamondClarityEnum.si2.value,
                DiamondClarityEnum.si2.value,
            ],
            DiamondColumnsEnum.COLOR.value: [
                DiamondColorEnum.h.value,
                DiamondColorEnum.h.value,
                DiamondColorEnum.h.value,
                DiamondColorEnum.h.value,
            ],
            DiamondColumnsEnum.CUT.value: [
                DiamondCutEnum.ideal.value,
                DiamondCutEnum.ideal.value,
                DiamondCutEnum.ideal.value,
                DiamondCutEnum.ideal.value,
            ],
            DiamondColumnsEnum.PRICE.value: [
                4733,
                1863,
                4325,
                2012,
            ],
        }

        return pd.DataFrame(data)

    @pytest.fixture
    def df_with_features_and_price(self):
        df_data = {
            DiamondColumnsEnum.CARAT.value: [
                1.1,
                0.83,
                1.03,
                0.78,
                2.02,
            ],
            DiamondColumnsEnum.CLARITY.value: [
                DiamondClarityEnum.si2.value,
                DiamondClarityEnum.si2.value,
                DiamondClarityEnum.si2.value,
                DiamondClarityEnum.si2.value,
                DiamondClarityEnum.si2.value,
            ],
            DiamondColumnsEnum.COLOR.value: [
                DiamondColorEnum.h.value,
                DiamondColorEnum.h.value,
                DiamondColorEnum.h.value,
                DiamondColorEnum.h.value,
                DiamondColorEnum.g.value,
            ],
            DiamondColumnsEnum.CUT.value: [
                DiamondCutEnum.ideal.value,
                DiamondCutEnum.ideal.value,
                DiamondCutEnum.ideal.value,
                DiamondCutEnum.ideal.value,
                DiamondCutEnum.very_good.value,
            ],
            DiamondColumnsEnum.PRICE.value: [4733, 1863, 4325, 2012, 12094],
        }
        return pd.DataFrame(df_data)

    @pytest.fixture
    def features(self):
        return DiamondFeaturesForSearchSchema(
            carat=0.6,
            cut=DiamondCutEnum.ideal.value,
            clarity=DiamondClarityEnum.si2.value,
            color=DiamondColorEnum.h.value,
        )

    class TestSearchDiamondByFeatures:

        def test_filter_diamonds_by_features(
            self,
            features,
            df_with_features_and_price,
            df_result_after_filter,
        ):

            response = filter_diamonds_by_features(
                features=features, df=df_with_features_and_price
            )

            assert isinstance(response, pd.DataFrame)
            assert_frame_equal(response, df_result_after_filter)

        def test_filter_diamonds_by_similar_weight(
            self,
            features,
            df_with_features_and_price,
            df_result_after_filter,
        ):

            response = diamonds_df_filtered_by_similar_weight(
                weight=features.carat, df=df_with_features_and_price
            )

            assert isinstance(response, pd.DataFrame)
            assert_frame_equal(response, df_result_after_filter)

        
