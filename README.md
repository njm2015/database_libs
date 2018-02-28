ALL DATABASES ARE CREATED IN THE FOLDER 1 LEVEL UP (../)

This library is used for retrieving and efficiently storing intraday minute data for equities. All core functions are found in the 'database_libs.py' file. The other files are wrappers that perform different functions:

	build_all.py -- reads all symbols in '../symlist.txt' and pulls minute data around 10-15 days back and stores this in sqlite database.

	build_db.py -- takes in one symbol name and creates an sqlite database. Then adds the symbol to '../symlist.txt'.

	update_all.py -- reads all symbols in '../symlist.txt' and inserts all information not already in the database for that company.

	update_db.py -- takes in one symbol and inserts information not already in teh database into that respective database. Will fail if database does not exist.

API used is alpha_vantage. Currently my api key is hard coded in, but in the future, I may uncomment the os code that imports an environment variable which has the key stored in it. alpha_vantage API keys are available for free at https://www.alphavantage.co/