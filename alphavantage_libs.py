import db_libs
import MySQLdb
import numpy as np
import openvpn
import pandas as pd
import random
import sys
import timeout

from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from tqdm import tqdm

date_format = '%Y-%m-%d %H:%M:%S'

symbol_file = '../tickers/symbol_list.csv'
exchange_file = '../tickers/exchanges.csv'
exchange_prefix = '../tickers/{}.csv'

log_filename = './log/' + datetime.now().strftime('%Y-%m-%d') + '.log'

api_keys = pd.read_csv('alphavantage.csv')['alphavantage_key'].values


def report_error(err_type, symb, err):
	with open(log_filename, 'a') as f:
		f.write(err_type + '\n')
		f.write(str(datetime.now()) + '\n')
		f.write(symb + '\n')
		f.write(str(err) + '\n')
		f.write('\n\n')
	return False


def connect_ts():
	return TimeSeries(key=random.choice(api_keys), output_format='pandas')


@timeout.timeout()
def get_intraday(symbol, ts=None):
	if ts is None:
		ts = connect_ts()
	try:
		return ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')
	except KeyError:
		print(symbol)
		raise RuntimeError



def update_symbol(symbol, ts=None, conn=None):
	try:
		df = get_intraday(symbol, ts)[0]
		df['index'] = df.index.map(lambda x: datetime.strptime(x, date_format))

		latest_date = db_libs.get_latest_entry(symbol, conn)
		latest_date = latest_date if latest_date is not None  else datetime.min
		mask = df.apply(lambda x: datetime.strptime(x.name, date_format) > latest_date, axis=1)

		db_libs.insert_1min_table(np.insert(df[mask].values, 0, symbol, axis=1))

		return True
	except (ValueError) as e:
		return report_error('ValueError', symbol, e)

	except (RuntimeError) as e:
		return report_error('RuntimeError', symbol, e)

	except (timeout.TimeoutError) as e:
		return report_error('TimeoutError', symbol, e)

	except Exception as e:
		return report_error('Unknown Error', symbol, e)



def build_symbol_file():
	exchanges = pd.read_csv(exchange_file)
	symbol_list = [
					{'listing' : symbol, 'exchange' : xchang} 
					for xchang in pd.read_csv(exchange_file)['name'].values
					for symbol in pd.read_csv(exchange_prefix.format(xchang))['Symbol'].values 
					if '^' not in symbol and '.' not in symbol
				]

	symbol_df = pd.DataFrame(symbol_list)
	symbol_df.to_csv(symbol_file)


def run():
	print(62)
	conn = db_libs.create_connection()

	symbol_list = np.unique(pd.read_csv(symbol_file)['listing'].values)
	np.random.shuffle(symbol_list)

	for i,symbol in tqdm(enumerate(symbol_list)):
		print(i,symbol)
		ts = connect_ts()
		if not update_symbol(symbol, connect_ts(), conn):
			ts = connect_ts()
		if i % 5 == 0:
			openvpn.change_server()
			ts = connect_ts()


if __name__ == '__main__':
	if openvpn.change_server():
		run()
	else:
		print(78)
	print(79)