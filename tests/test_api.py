import unittest

from fastapi.testclient import TestClient

from ml_models.linear_regression.backend.main import app


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_health_check(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_chart_data(self) -> None:
        response = self.client.get("/chart-data")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["points"]), 9)
        self.assertIn("slope_cop_per_m2", data)
        self.assertIn("intercept_cop", data)

    def test_prediction(self) -> None:
        response = self.client.post("/predict", json={"area_m2": 100})
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["area_m2"], 100)
        self.assertGreater(data["estimated_price_cop"], 0)
        self.assertEqual(data["currency"], "COP")

    def test_zero_area_is_rejected(self) -> None:
        response = self.client.post("/predict", json={"area_m2": 0})

        self.assertEqual(response.status_code, 422)

    def test_frontend_route_is_not_part_of_the_api(self) -> None:
        response = self.client.get("/app")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
