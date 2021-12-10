import pandas as pd
from datetime import datetime
from pprint import pprint

date_parse = lambda dates: [datetime.strptime(d, '%m/%d/%Y %I:%M:%S %p') for d in dates]
    

def load_consumption_csv(filename):
    return pd.read_csv(filename, parse_dates=['datetime_beginning_ept', 'datetime_beginning_utc'], date_parser=date_parse).to_dict('records')

if __name__ == '__main__':
    data = load_consumption_csv("test_data.csv")
    pprint(data)