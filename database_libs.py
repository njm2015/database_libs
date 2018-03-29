from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
#import os
import pandas as pd
import sqlite3
import sys

create_str = 'CREATE TABLE MINUTE_DATA(\
				ID INT PRIMARY KEY,\
				OPEN REAL,\
				HIGH REAL,\
				LOW REAL,\
				CLOSE REAL,\
				VOLUME REAL, \
				DATE_STR TEXT(20));'
latest_entry_str = 'SELECT ID FROM MINUTE_DATA \
					ORDER BY ID DESC LIMIT 1;'
count_entries_str = 'SELECT COUNT(*) AS ENTRIES \
					FROM MINUTE_DATA;'
insert_str = 'INSERT INTO MINUTE_DATA \
				VALUES (?,?,?,?,?,?,?)'
ep = datetime(1970, 1,1)
sym_filename = '../symlist.txt'

def usage():
	raise RuntimeError('<program_name> <symbol>')

def latest_entry(cursor):
	'''
		Retrieves latest entry from database
		@param cursor - cursor associated with respective database
	'''
	cursor.execute(latest_entry_str)
	return cursor.fetchone()

def count_entries(cursor):
	'''
		Returns the number of entries in the database
		@param cursor - cursor associated with respective database
	'''
	cursor.execute(count_entries_str)
	return cursor.fetchone()

def get_df(symbol):
	'''
		API call that retrieves the minute intraday data
		Commented line is to allow for api_key access through
		environment variables
		@param symbol - equity symbol to query
		@return pd.DataFrame with minute data
	'''
	#ts = TimeSeries(key=os.environ['APIKEY'], output_format='pandas')
	ts = TimeSeries(key='MP0WZA1RPICI6GTN', output_format='pandas')
	return ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')

def seconds_since_epoch(date_str):
	'''
		Returns the number of seconds between epoch and given
		date string.
	'''
	t = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
	return int((t-ep).total_seconds())

def data_list(df):
	'''
		Takes in pd.DataFrame and returns a list of lists of the columns
	'''
	return list(zip(df.index.tolist(), \
			df['1. open'].values.tolist(), \
			df['2. high'].values.tolist(), \
			df['3. low'].values.tolist(), \
			df['4. close'].values.tolist(), \
			df['5. volume'].values.tolist(), \
			df['date_str'].values.tolist()))

def create_db(filename):
	'''
		Creates an sqlite3 database with given filename
	'''
	conn = sqlite3.connect(filename)
	c = conn.cursor()

	# try-except block for testing purposes only
	try:
		c.execute('DROP TABLE MINUTE_DATA')
		c.execute(create_str)
	except sqlite3.OperationalError:
		c.execute(create_str)
	conn.commit()
	conn.close()

def insert_data(conn, cursor, df_list):
	'''
		Inserts given df_list into database with connection conn
		and cursor cursor.
	'''
	cursor.executemany(insert_str, df_list)
	conn.commit()

def read_file():
	'''
		Opens '../symlist.txt' and returns a list of the lines 
		of that file.
	'''
	with open(sym_filename, 'rt') as f:
		return [line[:-1] for line in f]

def write_file(symbol):
	'''
		Opens '../symlist.txt' and appends 'symbol' to a new line
		of the file
	'''
	with open(sym_filename, 'a+') as f:
		f.write(symbol + '\n')


