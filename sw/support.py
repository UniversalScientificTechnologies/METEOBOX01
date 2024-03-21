import pandas as pd
from datetime import datetime, timedelta
import requests
from io import StringIO

def generate_csv_urls(base_url_template, start_time, periods=6, freq='10min'):
    """
    Generuje seznam URL adres CSV souborů pro daný časový rozsah, včetně dynamického datumu v URL.
    """
    urls = []
    date_path = start_time.strftime("%Y/%m/%d/")
    base_url = base_url_template.format(date_path=date_path)
    
    for period in range(periods):
        time_stamp = start_time + timedelta(minutes=period*10)
        file_name = time_stamp.strftime("METEOBOX_export_%Y%m%d-%H%M%S.csv")
        urls.append(f"{base_url}{file_name}")
    return urls


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from io import StringIO
from tqdm import tqdm

def fetch_csv_urls(base_url):
    """
    Stáhne Apache index stránku a extrahuje odkazy na CSV soubory.
    """
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Najde všechny odkazy na stránce
    links = soup.find_all('a')
    csv_urls = [base_url + link.get('href') for link in links if link.get('href').endswith('.csv')]
    
    return csv_urls

def download_and_combine_csv(urls):
    """
    Stáhne CSV soubory z daných URL adres a sloučí je do jedné pandas DataFrame.
    """
    df_list = []
    for i, url in enumerate(tqdm(urls, desc="Downloading CSVs")):
        response = requests.get(url)
        if response.status_code == 200:
            csv_content = StringIO(response.content.decode('utf-8'))
            df = pd.read_csv(csv_content, skiprows=3, usecols=['_time', '_value', 'dataId', '_field'])
            df_list.append(df)
        else:
            print(f"Failed to download {url}")
    
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

def resample_sensor_data(combined_df):
    # Resample data for each sensor
    resampled_data = []
    unique_combinations = combined_df[['dataId', '_field']].drop_duplicates()
    for index, row in tqdm(unique_combinations.iterrows(), total=unique_combinations.shape[0], desc="Resampling data"):
        sensor = row['dataId']
        field = row['_field']
        sensor_data = combined_df[(combined_df['dataId'] == sensor) & (combined_df['_field'] == field)]
        # Convert _time to datetime
        sensor_data.loc[:, '_time'] = pd.to_datetime(sensor_data['_time'])
        resampled = sensor_data.resample('10T', on='_time').agg({'_value': 'mean', '_field': 'first'})
        resampled['dataId'] = sensor
        resampled_data.append(resampled)

    # Combine all resampled data
    resampled_df = pd.concat(resampled_data)

    # Reset index
    resampled_df.reset_index(inplace=True)

    return resampled_df

def pivot_sensor_data(resampled_df):
    # Pivot the DataFrame
    pivot_df = resampled_df.pivot_table(index='_time', columns=['dataId', '_field'], values='_value')
    pivot_df.columns = pivot_df.columns.map('_'.join)

    # Reset the index
    pivot_df.reset_index(inplace=True)

    return pivot_df

def main():
    date_path = datetime.now().strftime("%Y/%m/%d/")  # Dynamické generování cesty podle aktuálního data
    base_url = f"http://space.astro.cz/meteo/meteobox/meteobox_01/{date_path}"
    
    csv_urls = fetch_csv_urls(base_url)
    combined_df = download_and_combine_csv(csv_urls)
    print(combined_df.head())  # Zobrazí prvních několik řádků sloučené DataFrame
    # combined_df.to_csv("combined_data.csv", index=False)  # Volitelně uložit do souboru

if __name__ == "__main__":
    main()
