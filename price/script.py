import pandas as pd
from datetime import datetime
from pprint import pprint
from IPython import embed
import numpy as np
from sklearn.linear_model import LinearRegression

pd.options.display.float_format = '{:.2f}'.format

date_parse = lambda dates: [datetime.strptime(d, '%m/%d/%Y %I:%M:%S %p') for d in dates]
    
def load_csv_with_date(filename):
    return pd.read_csv(filename, parse_dates=['datetime_beginning_ept', 'datetime_beginning_utc'], date_parser=date_parse).to_dict('records')


class Data:
  def __init__(self):
    self.usage = []
    self.generation = {}

  
  def y(self):
    rates = []
    amount = []
    for row in self.usage:
      rates.append(row['dispatch_rate'])
      amount.append(row['actual_load'])
    return np.average(rates,weights=amount)
  '''
  def y(self):
    y = 0
    for row in self.usage:
      y += row['dispatch_rate'] * row['actual_load']
    return y
  '''

  def x(self):
    order = ['Coal','Gas','Hydro','Multiple Fuels','Nuclear','Oil',
      'Others','Other Renewables','Solar','Storage','Wind']

    f = lambda fuel: self.generation[fuel]['fuel_percentage_of_total'] if fuel in self.generation else 0

    percentages = [f(fuel) for fuel in order]
    return np.array(percentages)

  def __str__(self):
    sum_1 = sum(row['actual_load'] for row in self.usage)
    mw = sum(row['mw'] for row in self.generation.values())
    return str(self.usage) + ": " + str(sum_1) + "\n\n " + str(self.generation) + ": " + str(mw) + " \n\n"

  def __repr__(self):
      return str(self)



if __name__ == '__main__':
    gen_data = load_csv_with_date("gen_by_fuel.csv")
    by_date = {} 
    for row in gen_data:
        key = row['datetime_beginning_ept']
        if key not in by_date:
            by_date[key] = Data() 

        stripped_row = {
          'fuel_percentage_of_total' : row['fuel_percentage_of_total'],
          'mw' : row['mw']}
        by_date[key].generation[row['fuel_type']] = stripped_row


    ops_data = load_csv_with_date("ops_sum_prev_period.csv")
    for row in ops_data:
        key = row['datetime_beginning_ept']
        if key not in by_date:
            by_date[key] = Data() 
        
        stripped_row = {
            'dispatch_rate' : row['dispatch_rate'],
            'actual_load' : row['actual_load']}

        if row['actual_load'] == row['actual_load']: # NaNs
            by_date[key].usage.append(stripped_row)

    X = np.array([row.x() for row in by_date.values()])
    y = np.array([row.y() for row in by_date.values()])
    reg = LinearRegression(fit_intercept=False).fit(X, y)
    embed()
    #pprint(by_date)

    ## bounded regression
    ## scipy.optimize.lsq_linear(X, y, bounds=(15, 50), lsmr_tol='auto', verbose=1)
    