import unittest
from unittest.mock import patch, MagicMock
import datetime
from bs4 import BeautifulSoup

from utils.extract import fetching_content, extract_card_data, scrape_products


class TestExtractFunctions(unittest.TestCase):

    @patch('utils.extract.requests.Session.get')
    def test_fetching_content_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b'<html></html>'
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        url = 'http://example.com'
        result = fetching_content(url)
        self.assertEqual(result, b'<html></html>')
        mock_get.assert_called_once_with(url, headers=unittest.mock.ANY)

    @patch('utils.extract.requests.Session.get')
    def test_fetching_content_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response

        url = 'http://example.com'
        result = fetching_content(url)
        self.assertIsNone(result)

    def test_extract_card_data_success(self):
        html = '''
        <div class="product-details">
            <h3 class="product-title">Product A</h3>
            <div class="price">$100</div>
            <p>Rating: 4.5</p>
            <p>Colors: Red</p>
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        article = soup 

        result = extract_card_data(article)

        self.assertEqual(result['Title'], 'Product A')
        self.assertEqual(result['Price'], '$100')
        self.assertEqual(result['Rating'], '4.5')
        self.assertEqual(result['Colors'], 'Red')
        self.assertEqual(result['Size'], 'M')
        self.assertEqual(result['Gender'], 'Unisex')
        self.assertIsInstance(result['Timestamp'], datetime.datetime)

    def test_extract_card_data_missing_field(self):
        html = '<div></div>'
        soup = BeautifulSoup(html, 'html.parser')
        article = soup

        result = extract_card_data(article)
        self.assertIsNone(result)

    @patch('utils.extract.fetching_content')
    def test_scrape_products(self, mock_fetch):
        page1_html = '''
        <div class="collection-grid">
            <div class="collection-card">
                <div class="product-details">
                    <h3 class="product-title">Product 1</h3>
                    <div class="price">$50</div>
                    <p>Rating: 5</p>
                    <p>Colors: Blue</p>
                    <p>Size: L</p>
                    <p>Gender: Male</p>
                </div>
            </div>
        </div>
        <a class="page-link">Next</a>
        '''
        page2_html = '''
        <div class="collection-grid">
            <div class="collection-card">
                <div class="product-details">
                    <h3 class="product-title">Product 2</h3>
                    <div class="price">$60</div>
                    <p>Rating: 4</p>
                    <p>Colors: Green</p>
                    <p>Size: S</p>
                    <p>Gender: Female</p>
                </div>
            </div>
        </div>
        ''' 

        mock_fetch.side_effect = [page1_html.encode('utf-8'), page2_html.encode('utf-8')]

        base_url = 'http://fakeurl.com'
        data = scrape_products(base_url, delay=0)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['Title'], 'Product 1')
        self.assertEqual(data[1]['Title'], 'Product 2')

if __name__ == '__main__':
    unittest.main()
