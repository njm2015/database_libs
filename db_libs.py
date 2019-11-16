import db_queries
import MySQLdb
import os

db_filename = '../.intraday.db'

db_creds = {
	'host' : '127.0.0.1',
	'user' : 'nathaniel',
	'passwd' : 'templeton',
	'port' : 3306,
	'db' : 'main'
}

def create_connection():
	conn = MySQLdb.Connection(
		host=db_creds['host'],
		user=db_creds['user'],
		passwd=db_creds['passwd'],
		port=db_creds['port'],
		db=db_creds['db']
	)

	return conn


def create_1min_table(conn):
	conn.query(db_queries.create_1min_intraday_table)
	conn.commit()


def insert_1min_table(data, conn=None):
	if conn is None:
		conn = create_connection()

	cur = conn.cursor()
	cur.executemany(db_queries.insert_query, data.tolist())
	conn.commit()


def get_latest_entry(symbol, conn=None):
	if conn is None:
		conn = create_connection()

	cur = conn.cursor()
	cur.execute(db_queries.latest_entry_query, (symbol,))
	try:
		return cur.fetchone()[0]
	except TypeError:
		return None

if __name__ == '__main__':
	#create_1min_table(create_connection())
	print(get_latest_entry('AAPL'))