
import sqlite3
from sys import argv

if len(argv) != 2:
		print 'usuage\n\tpython',argv[0],'<table_name>'
		exit(1)
else:
	table_name = argv[1]

db = sqlite3.connect( 'logs/data.db' )
cursor = db.cursor()

sql_query = """
SELECT
	state,
	COUNT(url)
FROM
	{}
WHERE
	country is 'United States'
GROUP BY
	state
ORDER BY
	COUNT(url) desc;
""".format(table_name)

for row in cursor.execute(sql_query):
	print row

cursor.close()
db.close()