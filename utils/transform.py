import pandas as pd
import re

def transform_to_DataFrame(data):
    """
    Mengubah data menjadi DataFrame.
    """

    try:
        df = pd.DataFrame(data)
        print('Data berhasil diubah ke DataFrame')

        return df
    except Exception as e:
        print(f'Terjadi kesalahan dalam transform to DataFrame: {e}')

def transform_data(data, exchange_rate):
    """
    Menggabungkan semua transformasi data menjadi satu fungsi.
    """

    try:
        data['Rating'] = data['Rating'].apply(
            lambda text: float(re.search(r'(\d+(\.\d+)?)\s*/\s*5', text).group(1)) if re.search(r'(\d+(\.\d+)?)\s*/\s*5', text) else 0
        )

        dirty_patterns = {
            "Title" : ["Unknown Product"],
            "Rating" : ["Invalid rating", "Not Rated"],
            "Price" : ["Price Unavailable", None]
        }

        for column, patterns in dirty_patterns.items():
            data = data[~data[column].isin(patterns)]

        data['Price'] = data['Price'].str.replace('$', '').astype(float)
        data['Price'] = data['Price'] * exchange_rate
        data['Colors'] = data['Colors'].str.replace(' Colors', '')
        
        data['Title'] = data['Title'].astype('object')
        data['Price'] = data['Price'].astype(float)
        data['Rating'] = data['Rating'].astype(float)
        data['Colors'] = data['Colors'].astype(int)
        data['Size'] = data['Size'].astype('object')
        data['Gender'] = data['Gender'].astype('object')
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])

        data.drop_duplicates()
        data.dropna()
        
        print('Data berhasil ditransformasi')
        return data
    except Exception as e:
        print(f'Terjadi kesalahan dalam transform data: {e}')
        