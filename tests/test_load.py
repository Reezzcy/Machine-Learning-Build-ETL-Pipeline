import unittest
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
import os

from utils import load

class TestLoadFunctions(unittest.TestCase):

    @patch('utils.load.create_engine')
    def test_store_to_postgre(self, mock_create_engine):
        df = pd.DataFrame({'Title': ['Item A'], 'Price': [100]})

        mock_engine = MagicMock()
        mock_connection = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_create_engine.return_value = mock_engine

        load.store_to_postgre(df, 'dummy_postgre_url')

        mock_create_engine.assert_called_once_with('dummy_postgre_url')
        mock_engine.connect.assert_called_once()

    @patch('utils.load.os.path.abspath')
    @patch('utils.load.os.path.join')
    @patch('pandas.DataFrame.to_csv')
    def test_store_to_csv(self, mock_to_csv, mock_join, mock_abspath):
        df = pd.DataFrame({'Title': ['Item B'], 'Price': [200]})
        mock_abspath.return_value = '/fake/path'
        mock_join.return_value = '/fake/path/products.csv'

        load.store_to_csv(df, 'products.csv')
        mock_to_csv.assert_called_once_with('/fake/path/products.csv', index=False)

    @patch('utils.load.build')
    @patch('utils.load.Credentials.from_service_account_file')
    @patch('builtins.open', new_callable=mock_open, read_data="Title,Price\nItem C,150\n")
    @patch('utils.load.csv.reader')
    @patch('utils.load.os.path.abspath')
    @patch('utils.load.os.path.join')
    def test_store_to_googlesheets(self, mock_join, mock_abspath, mock_csv_reader, mock_open_file, mock_creds, mock_build):
        mock_abspath.return_value = '/fake/base'
        mock_join.side_effect = lambda *args: '/'.join(args)

        mock_creds.return_value = MagicMock()

        mock_csv_reader.return_value = iter([['Title', 'Price'], ['Item C', '150']])

        mock_service = MagicMock()
        mock_sheet = MagicMock()
        mock_service.spreadsheets.return_value = mock_sheet
        mock_build.return_value = mock_service

        mock_sheet.values.return_value.update.return_value.execute.return_value = {}

        load.store_to_googlesheets('products.csv')

        mock_build.assert_called_once()
        mock_sheet.values.return_value.update.assert_called_once()

if __name__ == '__main__':
    unittest.main()
