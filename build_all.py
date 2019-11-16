import database_libs as dl
import pandas as pd
import MySQLdb

def build_from_symbol(_sym):

	filename = '../' + _sym + '.db'
	min_df, meta_data = dl.get_df(_sym)
	min_df['date_str'] = min_df.index
	min_df.index = pd.Series(min_df.index.map(dl.seconds_since_epoch))
	min_df['5. volume'] = min_df['5. volume'].astype(int)

	dl.create_db(filename)
	df_list = dl.data_list(min_df)

	conn = sqlite3.connect(filename)
	c = conn.cursor()

	dl.insert_data(conn, c, df_list)
	conn.close()

	print('%s created' % (filename))

if __name__ == '__main__':
	sym_list = dl.read_file()

	for sym in sym_list:
		build_from_symbol(sym)