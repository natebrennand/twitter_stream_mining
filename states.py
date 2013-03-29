
import sqlite3

db = sqlite3.connect( 'logs/data.db' )
cursor = db.cursor()

cursor.execute( """
SELECT 
	name
FROM 
	sqlite_master 
WHERE
	sql NOT NULL;""" )
table_list = cursor.fetchone()

for table in table_list:
	print '\nTable: ',table
	sql_query = """
	SELECT
		COUNT(url),
		state
	FROM
		{}
	WHERE
		country is 'United States'
	GROUP BY
		state
	ORDER BY
		COUNT(url) desc;
	""".format(table)

	for row in cursor.execute(sql_query):
		print row[0],'\t',row[1].encode('ascii','ignore')

cursor.close()
db.close()
