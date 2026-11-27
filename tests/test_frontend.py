import os
import unittest
from unittest.mock import patch

from ml_models.linear_regression.frontend.main import app


class FrontendTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

    def test_frontend_page_is_served(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)
        response.close()

    def test_static_assets_are_served(self) -> None:
        response = self.client.get("/static/style.css")

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/css", response.content_type)
        response.close()

    def test_config_exposes_backend_url_without_caching(self) -> None:
        with patch.dict(os.environ, {"BACKEND_URL": "https://api.example.test/"}):
            response = self.client.get("/config.js")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'window.CASAVALOR_API_URL = "https://api.example.test";',
            response.get_data(as_text=True),
        )
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_config_reports_missing_backend_url(self) -> None:
        with patch.dict(os.environ):
            os.environ.pop("BACKEND_URL", None)
            response = self.client.get("/config.js")

        self.assertEqual(response.status_code, 503)
