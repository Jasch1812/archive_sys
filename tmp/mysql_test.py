import MySQLdb as sql

conn = sql.connect(host='localhost', port=3306, user='root', passwd='12345678', db = 'test1')
cur = conn.cursor()
cur.execute('SELECT * FROM potluck')
# cur.execute('SHOW DATABASES;')
# print cur.description
for row in cur.fetchall():
    print row
    
cur.close()
conn.close()
