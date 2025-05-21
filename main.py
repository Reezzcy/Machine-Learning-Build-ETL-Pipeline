from utils.extract import scrape_products
from utils.transform import transform_to_DataFrame, transform_data
from utils.load import store_to_postgre, store_to_csv, store_to_googlesheets

def main():
    """
    Fungsi utama untuk keseluruhan proses scraping, transformasi data, dan penyimpanan.
    """

    BASE_URL = 'https://fashion-studio.dicoding.dev'
    
    all_cloth_data = scrape_products(BASE_URL)
    
    if all_cloth_data:
        try:
            df = transform_to_DataFrame(all_cloth_data)
            df = transform_data(df, 16000)

            filename = 'products.csv'

            store_to_csv(df, filename)

            db_url = 'postgresql+psycopg2://developer:supersecret@localhost:5432/submissionfda'
            store_to_postgre(df, db_url)

            store_to_googlesheets(filename)

        except Exception as e:
            print(f"Terjadi kesalahan dalam proses: {e}")
    else:
        print("Tidak ada data yang ditemukan.")

if __name__ == '__main__':
    main()
