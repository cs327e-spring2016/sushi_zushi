
#First we want to import the programs we need to do our webscrapping and pymysql
from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import pymysql
import json
#Here we are connectig to my sql.
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='', db='billboard')
cur = conn.cursor()
#cur.execute("USE ")

#This is the code to import our values to our table in sql
def store(artist_name2):

	cur.execute("""INSERT INTO artist (artist_name) VALUES({0})""".format(json.dumps(artist_name2)))
	cur.connection.commit()

#Here we are checking if there are any repeated values in the table so that it doesn't import them twice.
def check(name):
	test = False
	test1 = cur.execute("""SELECT * FROM artist WHERE artist_name = ({0})""".format(json.dumps(name)))
	if test1 == 1:
		return True
	else:
		return False

#Here we are doing our webscrapping.

def getLinks(articleUrl):
	bsObj = BeautifulSoup(html)
	nameList1 = bsObj.findAll("",{"class":"chart-row__artist"})
	for name in nameList1:
		name = name.get_text()
		name= name.strip()
		if check(name) != True:
			store(name)

#These are the different URL's for the different dates. 

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
html = urlopen("http://www.billboard.com/charts/hot-100/2016-04-23")

#Here the function is called 
getLinks(html)


cur.close()
conn.close()