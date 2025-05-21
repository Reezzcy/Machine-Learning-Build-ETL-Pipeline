import os, csv
from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def store_to_postgre(data, db_url):
    """
    Fungsi untuk menyimpan data ke dalam PostgreSQL.
    """

    try:
        engine = create_engine(db_url)
        
        with engine.connect() as con:
            data.to_sql('products', con=con, if_exists='replace', index=False)
            print("Data berhasil disimpan ke Postgre!")
    
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke Postgre: {e}")

def store_to_csv(data, filename):
    """
    Fungsi untuk menyimpan data ke CSV
    """

    try:
        BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        FILE_PATH = os.path.join(BASE_PATH, filename)

        data.to_csv(FILE_PATH, index=False)
        print("Data berhasil disimpan ke CSV!")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke CSV: {e}")

def store_to_googlesheets(filename):
    """
    Fungsi untuk menyimpan data ke Google Sheets
    """

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'your_spread_sheet_api.json')
    CSV_PATH = os.path.join(BASE_DIR, filename)

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    SPREADSHEET_ID = 'your_spread_sheet_id'
    RANGE_NAME = 'Sheet1!A2:G868'

    try:
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()

        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            values = list(reader)

        body = {
            'values': values
        }

        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()

        print("Data berhasil disimpan ke Google Spreadsheets!")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke Google Spreadsheets: {e}")
