import sqlite3

con = sqlite3.connect('makan.db')

cur = con.cursor()

for row in cur.execute('SELECT * FROM food'):
    print(row)
con.close()
