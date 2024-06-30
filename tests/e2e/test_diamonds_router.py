import pytest

class TestPostPredictedDiamondPrice:
    @pytest.mark.db
    def test_post_predicted_diamond_price(self, mocker, client):
        mocker.patch(
            "src.services.diamond_service.predict_diamond_price",
            return_value="The predicted value for the diamond is: $5358.2705078125",
        )

        mocker.patch("src.services.api_requests_service.save_api_requests_to_database")
        data = {
            "carat": 1,
            "cut": "Fair",
            "color": "D",
            "clarity": "IF",
            "depth": 1,
            "table": 1,
            "x": 1,
            "y": 1,
            "z": 1,
        }
        response = client.post("/diamond/predict-price", json=data)

        assert response is not None
        assert (
            response.json()
            == "The predicted value for the diamond is: $5358.2705078125"
        )

    @pytest.mark.parametrize(
        "body_data",
        [
            (
                {
                    "carat": 0,
                    "cut": "Fair",
                    "color": "D",
                    "clarity": "IF",
                    "depth": 1,
                    "table": 1,
                    "x": 1,
                    "y": 1,
                    "z": 1,
                }
            ),
            (
                {
                    "carat": 1,
                    "cut": "Fair",
                    "color": "D",
                    "clarity": "IF",
                    "depth": 0,
                    "table": 1,
                    "x": 1,
                    "y": 1,
                    "z": 1,
                }
            ),
        ],
    )
    def test_raises_400_when_body_data_has_0_values(self, body_data, client):

        response = client.post("/diamond/predict-price", json=body_data)

        assert response.status_code == 400


class TestPostSearchDiamondByFeaturesAndSimilarWeight:
    def test_post_search_diamond_by_features_and_similar_weight(self, client):
        data = {"carat": 0.96, "cut": "Ideal", "color": "H", "clarity": "SI2"}

        response = client.post("/diamond/search", json=data)

        assert response is not None
        assert response.status_code == 200

    def test_raises_400_when_there_is_no_results(self, client):
        data = {"carat": 1, "cut": "Fair", "color": "D", "clarity": "IF"}

        response = client.post("/diamond/search", json=data)

        assert response.status_code == 400
        assert (
            response.json()["detail"]
            == "It was not found diamonds for the chosen features."
        )

    def test_raises_400_when_carat_is_zero(self, client):
        data = {"carat": 0, "cut": "Fair", "color": "D", "clarity": "IF"}

        response = client.post("/diamond/search", json=data)

        assert response.status_code == 400
        assert response.json()["detail"] == "carat must have value grather than 0."
