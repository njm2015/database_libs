create_1min_intraday_table = '''
create table intraday_1min (
	dtime datetime,
	symbol varchar(10),
	open double,
	high double,
	low double,
	close double,
	volume int,
	primary key (dtime, symbol)
);
'''

insert_query = '''
insert into intraday_1min (
	symbol,
	open,
	high,
	low,
	close,
	volume,
	dtime
)
values
	(%s, %s, %s, %s, %s, %s, %s)
'''

latest_entry_query = '''
select dtime
from intraday_1min
where symbol=%s
order by dtime desc
'''