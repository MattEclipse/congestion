# This script extract datas from the API ENTSOE
# between start_date and end_date
# for dataset related to power plant generation in country_code
# it stores .csv file

from entsoe import EntsoePandasClient, EntsoeRawClient 
import pandas as pd
from dateutil.relativedelta import relativedelta
import time
import numpy as np
rng = np.random.standard_normal(2)  

client_raw = EntsoeRawClient(api_key='4aa04087-0e00-4997-81c5-4f5c5c5881ef')
client_pd = EntsoePandasClient(api_key= '4aa04087-0e00-4997-81c5-4f5c5c5881ef')

start_str = '20230101'
start = pd.Timestamp(start_str, tz='Europe/Brussels')
end_str = '20230301' # 20241001
end = pd.Timestamp(end_str, tz='Europe/Brussels')

countries = ['FR'] 

for country_code in countries:
    dataframes = []
    current_date = start

    while current_date < end:
        next_date = current_date + relativedelta(days=2)
        
        # Query data for the current month
        df = client_pd.query_generation_per_plant(
            country_code=country_code,
            start=current_date,
            end=next_date,
            psr_type=None
        )
        
        # Append the DataFrame to the list
        dataframes.append(df)
        
        # Move to the next month
        current_date = next_date

    # Concatenate all DataFrames into one
    final_df = pd.concat(dataframes, ignore_index=False)
    path_data_csv = "/Users/matthiasmolenat/repos/congestion/data/gen_plant_from_" + start_str + '_to_' + end_str+ "_"+country_code+".csv"
    final_df.to_csv(path_data_csv)
    
    time.sleep(rng.random())
    

