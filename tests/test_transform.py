import unittest
import pandas as pd
from utils.transform import transform_to_DataFrame, transform_data

class TestTransformFunctions(unittest.TestCase):

    def test_transform_to_DataFrame_valid(self):
        data = [{'Title': 'Product A', 'Price': '$10.00'}]
        df = transform_to_DataFrame(data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.iloc[0]['Title'], 'Product A')

    def test_transform_data_valid(self):
        raw_data = pd.DataFrame({
            'Title': ['Product A', 'Unknown Product'],
            'Rating': ['4.5 / 5', 'Invalid rating'],
            'Price': ['$10.00', 'Price Unavailable'],
            'Colors': ['5 Colors', '3 Colors'],
            'Size': ['M', 'L'],
            'Gender': ['Unisex', 'Male'],
            'Timestamp': ['2024-01-01', '2024-02-01']
        })

        exchange_rate = 15000

        cleaned = transform_data(raw_data, exchange_rate)

        self.assertIsInstance(cleaned, pd.DataFrame)
        self.assertIn('Title', cleaned.columns)
        self.assertEqual(cleaned.shape[0], 1)
        self.assertAlmostEqual(cleaned.iloc[0]['Price'], 150000.0)
        self.assertEqual(cleaned.iloc[0]['Colors'], 5)
        self.assertEqual(cleaned.iloc[0]['Rating'], 4.5)

    def test_transform_data_with_invalid_rating_format(self):
        raw_data = pd.DataFrame({
            'Title': ['Product A'],
            'Rating': ['Excellent'],
            'Price': ['$20.00'],
            'Colors': ['3 Colors'],
            'Size': ['L'],
            'Gender': ['Male'],
            'Timestamp': ['2024-01-01']
        })

        exchange_rate = 15000
        transformed = transform_data(raw_data, exchange_rate)
        self.assertEqual(transformed.iloc[0]['Rating'], 0.0)

if __name__ == '__main__':
    unittest.main()
