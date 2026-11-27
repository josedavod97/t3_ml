import tempfile
import unittest
from pathlib import Path

import pandas as pd

from ml_models.random_forest.model_utils import cargar_o_entrenar_modelo


class RandomForestModelTests(unittest.TestCase):
    def test_trains_and_saves_model_when_model_file_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            dataset_path = temp_path / "dataset.csv"
            model_path = temp_path / "models" / "model.pkl"
            pd.DataFrame({
                "edad": [20, 25, 60, 65],
                "diagnostico": ["gripe", "gripe", "infarto", "infarto"],
            }).to_csv(dataset_path, index=False)

            model = cargar_o_entrenar_modelo(model_path, dataset_path)

            self.assertTrue(model_path.is_file())
            self.assertEqual(list(model.feature_names_in_), ["edad"])

    def test_reports_missing_dataset_when_model_is_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            with self.assertRaises(FileNotFoundError):
                cargar_o_entrenar_modelo(
                    temp_path / "models" / "model.pkl",
                    temp_path / "missing.csv",
                )


if __name__ == "__main__":
    unittest.main()
