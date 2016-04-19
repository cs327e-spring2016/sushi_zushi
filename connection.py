import pymysql
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',user='root', passwd='', db='bank')
cur = conn.cursor()
cur.execute("SELECT * FROM account")
print(cur.fetchone())
cur.close()
conn.close()