import database_libs as dl
import pandas as pd
import sqlite3
import sys

if __name__ == '__main__':
	if len(sys.argv) < 2:
		dl.usage()

	filename = '../' + sys.argv[1] + '.db'

	min_df, meta_data = dl.get_df(sys.argv[1])
	min_df['date_str'] = min_df.index
	min_df.index = pd.Series(min_df.index.map(dl.seconds_since_epoch))
	min_df['5. volume'] = min_df['5. volume'].astype(int)

	conn = sqlite3.connect(filename)
	c = conn.cursor()

	le = dl.latest_entry(c)

	prev_entries_num = dl.count_entries(c)

	df_list = dl.data_list(min_df[min_df.index > le[0]])

	dl.insert_data(conn, c, df_list)

	curr_entries_num = dl.count_entries(c)
	conn.close()
	
	print('%d entries added' % (curr_entries_num[0] - prev_entries_num[0]))