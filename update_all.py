import database_libs as dl
import pandas as pd
import sqlite3

from build_all import build_from_symbol

if __name__ == '__main__':
	
	sym_list = dl.read_file()

	for sym in sym_list:
		filename = '../' + sym + '.db'

		min_df, meta_data = dl.get_df(sym)
		min_df['date_str'] = min_df.index
		min_df.index = pd.Series(min_df.index.map(dl.seconds_since_epoch))
		min_df['5. volume'] = min_df['5. volume'].astype(int)

		conn = sqlite3.connect(filename)
		c = conn.cursor()

		try:
			le = dl.latest_entry(c)
		except sqlite3.OperationalError:
			conn.close()
			build_from_symbol(sym)
			conn = sqlite3.connect(filename)
			c = conn.cursor()

			le = dl.latest_entry(c)

		prev_entries_num = dl.count_entries(c)

		df_list = dl.data_list(min_df[min_df.index > le[0]])

		dl.insert_data(conn, c, df_list)

		curr_entries_num = dl.count_entries(c)
		conn.close()
		
		print('%d entries added to %s' % (curr_entries_num[0] - prev_entries_num[0], filename))