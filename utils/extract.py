import time
import datetime
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
} 

def fetching_content(url):
    """
    Mengambil konten HTML dari URL yang diberikan.
    """

    session = requests.Session()
    response = session.get(url, headers=HEADERS)

    try:
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None
    except Exception as e:
        print(f"Tidak dapat terhubung dengan halaman: {e}")

def extract_card_data(article):
    """
    Mengambil data products berupa judul, harga, rating, warna, ukuran, gender, timestamp dari element html.
    """

    try:
        product = article.find('div', class_='product-details')
        title = product.find('h3', class_='product-title').text.strip()
        price = product.find(class_='price').text.strip()

        values = []
        p_tags = product.find_all('p')
        for p in p_tags:
            text = p.get_text(strip=True)
            if ':' in text:
                _, value = text.split(':', 1)
                value = value.strip()
            else:
                value = text.strip()

            values.append(value)

        product_data = {
            'Title': title,
            'Price': price,
            'Rating': values[0],
            'Colors': values[1],
            'Size': values[2],
            'Gender': values[3],
            'Timestamp' : datetime.datetime.now()

        }

        return product_data
    except Exception as e:
        print(f'Terjadi kesalahan saat mengekstrak data: {e}')

def scrape_products(base_url, start_page=1, delay=2):
    """
    Fungsi utama untuk mengambil keseluruhan data, mulai dari requests hingga menyimpannya dalam variabel data.
    """
    
    data = []
    page_number = start_page

    try:
        while True:
            url = base_url if page_number == 1 else f'{base_url}/page{page_number}'
            print(f"Scraping halaman: {url}")

            content = fetching_content(url)
            if content:
                soup = BeautifulSoup(content, "html.parser")
                card_grid = soup.find('div', class_='collection-grid')
                card_element = card_grid.find_all('div', class_='collection-card')

                for card in card_element:
                    data_card = extract_card_data(card)
                    data.append(data_card)

                next_button = soup.find('a', class_='page-link', string='Next')
                if next_button:
                    page_number += 1
                    time.sleep(delay)
                else:
                    break
            else:
                break
        
        print('Halaman berhasil discrape')
        return data
    except Exception as e:
        print(f'Terjadi kesalahan saat mengekstrak Page: {e}')
