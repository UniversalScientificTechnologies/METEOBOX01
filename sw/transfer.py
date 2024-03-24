import argparse
from datetime import datetime, timedelta
import support

# Tento program stahuje data z METEOBOX přes Apache index a data sloučí do jednoho CSV souboru.

def parse_args():
    """
    Zpracovává argumenty z příkazové řádky.

    Returns:
        tuple: Tuple obsahující počáteční a koncové datum nebo konkrétní datum.
    """
    parser = argparse.ArgumentParser(description='Stahování dat z Meteobox01 API')
    parser.add_argument('--start', type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                        help='Počáteční datum intervalu dat (RRRR-MM-DD)')
    parser.add_argument('--end', type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                        help='Koncové datum intervalu dat (RRRR-MM-DD)')
    parser.add_argument('--date', type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                        help='Konkrétní datum dat (RRRR-MM-DD)')
    args = parser.parse_args()

    if args.start and args.end:
        if args.date:
            parser.error('Nelze zadat současně počáteční/koncové datum a konkrétní datum')
        return args.start, args.end
    elif args.date:
        return args.date, args.date
    else:
        parser.error('Musíte zadat buď počáteční/koncové datum nebo konkrétní datum')

start_date, end_date = parse_args()

current_date = start_date
while current_date <= end_date:
    date_path = current_date.strftime("%Y/%m/%d/")
    base_url = f"http://space.astro.cz/meteo/meteobox/meteobox_01/{date_path}"
    print(base_url)  # Vypíše URL adresu, která bude použita pro stažení CSV souborů

    csv_urls = support.fetch_csv_urls(base_url)
    #print(csv_urls)  # Vypíše seznam URL adres CSV souborů, které budou staženy a sloučeny

    combined_df = support.download_and_combine_csv(csv_urls)
    print(combined_df.head())  # Zobrazí prvních několik řádků sloučené DataFrame

    resampled_df = support.resample_sensor_data(combined_df)

    pivot_df = support.pivot_sensor_data(resampled_df)

    pivot_df.to_csv("combined_data_{}.csv".format(date_path.replace('/', '_')), index=True)

    # Increment the current date by one day
    current_date += timedelta(days=1)
