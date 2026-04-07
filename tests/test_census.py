import unittest
from pathlib import Path

from serenipy.census import CensusLine, ExperimentLine, from_census, to_df

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class TestCensus(unittest.TestCase):
    def test_from_census(self):
        with open(DATA_DIR / "census.txt", "r") as file:
            header_lines, census_lines = from_census(file)

        self.assertIsInstance(header_lines, list)
        self.assertGreater(len(header_lines), 0)
        self.assertTrue(all(isinstance(h, str) for h in header_lines))

        self.assertIsInstance(census_lines, list)
        self.assertGreater(len(census_lines), 0)

        first = census_lines[0]
        self.assertIsInstance(first, CensusLine)
        self.assertIsInstance(first.norm_intensities, list)
        self.assertIsInstance(first.experiment_lines, list)
        self.assertGreater(len(first.experiment_lines), 0)
        self.assertIsInstance(first.experiment_lines[0], ExperimentLine)

    def test_census_to_df(self):
        import pandas as pd

        with open(DATA_DIR / "census.txt", "r") as file:
            df = to_df(file)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
        self.assertGreater(len(df.columns), 0)
