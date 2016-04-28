#Here we are connecting to mysql and importing the programs we need.

from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import pymysql
import json
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='', db='billboard')
cur = conn.cursor()


#Here we are adding the values into our tables

def store(song_name2):

	cur.execute("""INSERT INTO song (song_name) VALUES({0})""".format(json.dumps(song_name2)))
	cur.connection.commit()

#Here we are checking for repeated values
def check(name):
	test = False
	test1 = cur.execute("""SELECT * FROM song WHERE song_name = ({0})""".format(json.dumps(name)))
	if test1 == 1:
		return True
	else:
		return False

#Here we are doing our webscrapping

def getLinks(articleUrl):
	bsObj = BeautifulSoup(html)
	nameList1 = bsObj.findAll("",{"class":"chart-row__song"})
	songs = []
	for name in nameList1:
		name = name.get_text()
		if check(name) != True:
		
			store(name)
	
#Here are the different urls we need to gather our data.

#html = urlopen("http://www.billboard.com/charts/hot-100/2016-01-02")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-01-09")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-01-16")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-01-23")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-01-30")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-02-06")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-02-13")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-02-20")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-02-27")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-03-05")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-03-12")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-03-19")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-03-26")
#html= urlopen("http://www.billboard.com/charts/hot-100/2016-04-02")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-04-09")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-04-16")
#html = urlopen("http://www.billboard.com/charts/hot-100/2016-04-23")
getLinks(html)


cur.close()
conn.close()