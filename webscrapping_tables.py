
#First we want to import the programs we need to do our webscrapping and pymysql
from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import pymysql
import json
#Here we are connectig to my sql.
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='', db='billboard')
cur = conn.cursor()
#cur.execute("USE ")

#This is the code to import our artis value to our table in sql
def store_artist(artist_name2):
    #Here we are storing the values for the artist table.
	cur.execute("""INSERT INTO artist (artist_name) VALUES({0})""".format(json.dumps(artist_name2)))
	cur.connection.commit()

#This is our code to import our song value into the table in sql
def store_song(song_name2):
	cur.execute("""INSERT INTO song (song_name) VALUES({0})""".format(json.dumps(song_name2)))
	cur.connection.commit()

#Here we are checking if there are any repeated values in the table so that it doesn't import them twice.
def check_artist(name):
	test = False
	test1 = cur.execute("""SELECT * FROM artist WHERE artist_name = ({0})""".format(json.dumps(name)))
	if test1 == 1:
		return True
	else:
		return False

#Here we are going to check if the song is repeated before we append it.
def check_song(name):
	test = False
	test1 = cur.execute("""SELECT * FROM song WHERE song_name = ({0})""".format(json.dumps(name)))
	if test1 == 1:
		return True
	else:
		return False

#This is creating the junction table.

def check_sa(song,artist):

	test1 = cur.execute("SELECT * FROM artist_song WHERE artist_id = (SELECT artist_id FROM artist WHERE artist_name = %s) AND  song_id = (SELECT song_id FROM song WHERE song_name = %s)",(song,artist))
	if test1 == 1:
		return True
	else:
		return False

def store_sa(artist_name2,song_name2):
	cur.execute("INSERT INTO artist_song (artist_id,song_id) VALUES ((SELECT artist_id FROM artist WHERE artist_name= %s ), (SELECT song_id FROM song WHERE song_name =%s ))",(artist_name2,song_name2))
	cur.connection.commit()


#Here we are storing the values we fetched to mysql
def store_top100(week,rank,artist_name2,song_name2):

	cur.execute("INSERT INTO top100 (week_id, rank, comp_id) VALUES ((SELECT week_id FROM week WHERE week_id= %s ), (%s), (SELECT comp_id FROM artist_song WHERE artist_id = (SELECT artist_id FROM artist WHERE artist_name = %s) AND song_id = (SELECT song_id FROM song WHERE song_name = %s)))",(week,rank,artist_name2,song_name2))
	cur.connection.commit()

#Here we are doing our webscrapping.

def getLinks(articleUrl,week):
	bsObj = BeautifulSoup(articleUrl, "html.parser")
	nameList1 = bsObj.findAll("",{"class":"chart-row__artist"})
	nameList2 = bsObj.findAll("",{"class":"chart-row__song"})
	rank = bsObj.findAll("",{"class":"chart-row__current-week"})
	list1=[]
	list2=[]
	list3=[]
	for name in nameList1:
		name = name.get_text()
		name= name.strip()
		list1.append(name)
		if check_artist(name) != True:
			store_artist(name)
	for name in nameList2:
		name=name.get_text()
		name=name.strip()
		list2.append(name)
		if check_song(name) != True:
			store_song(name)

	for number in rank:
		number = number.get_text()
		number=number.strip()
		list3.append(number)

	matrix1 = []
	matrix2 = []
	for i in range(len(list1)):
		matrix1.append([list1[i],list2[i]])
		matrix2.append([list3[i],list1[i],list2[i]])
	for i in matrix1:
		if check_sa(i[0],i[1]) != True:
			store_sa(i[0],i[1])
	for i in matrix2:
			store_top100(week,i[0],i[1],i[2])




#These are the different URL's for the different dates. 

html1 = urlopen("http://www.billboard.com/charts/hot-100/2016-01-02")
html2 = urlopen("http://www.billboard.com/charts/hot-100/2016-01-09")
html3 = urlopen("http://www.billboard.com/charts/hot-100/2016-01-16")
html4 = urlopen("http://www.billboard.com/charts/hot-100/2016-01-23")
html5 = urlopen("http://www.billboard.com/charts/hot-100/2016-01-30")
html6 = urlopen("http://www.billboard.com/charts/hot-100/2016-02-06")
html7= urlopen("http://www.billboard.com/charts/hot-100/2016-02-13")
html8 = urlopen("http://www.billboard.com/charts/hot-100/2016-02-20")
html9 = urlopen("http://www.billboard.com/charts/hot-100/2016-02-27")
html10 = urlopen("http://www.billboard.com/charts/hot-100/2016-03-05")
html11 = urlopen("http://www.billboard.com/charts/hot-100/2016-03-12")
html12 = urlopen("http://www.billboard.com/charts/hot-100/2016-03-19")
html13 = urlopen("http://www.billboard.com/charts/hot-100/2016-03-26")
html14= urlopen("http://www.billboard.com/charts/hot-100/2016-04-02")
html15 = urlopen("http://www.billboard.com/charts/hot-100/2016-04-09")
html16 = urlopen("http://www.billboard.com/charts/hot-100/2016-04-16")
html17 = urlopen("http://www.billboard.com/charts/hot-100/2016-04-23")
songlist=[html1,html2,html3,html4,html5,html6,html7,html8,html9,html10,html11,html12,html13,html14,html15,html16,html17]

#Here the function is called 
week_number = 1
for i in songlist:
	getLinks(i,week_number)
	#week_number = int(week_number)
	week_number = week_number + 1
	#week_number = str(week_number)


cur.close()
conn.close()