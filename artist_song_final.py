#Connecting to my sql and importing the programs that we need.
from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import pymysql
import json
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='', db='billboard')
cur = conn.cursor()
#cur.execute("USE ")

#Here we are adding our values to our table
def store1(artist_name2,song_name2):

	#cur.execute("INSERT INTO song (song_amount, song_name) VALUES ((\"%s\",\"%s\")", (song_id, song_name)) 
	#t = (song_id2, song_name2)
	#cur.execute("""INSERT INTO artist_song (name_artist,name_song) VALUES({1})""".format(json.dumps(artist_name2,song_name2)))
	cur.execute("INSERT INTO artist_song (artist_id,song_id) VALUES ((SELECT artist_id FROM artist WHERE artist_name= %s ), (SELECT song_id FROM song WHERE song_name =%s ))",(artist_name2,song_name2))
	cur.connection.commit()

#Here we are checking for repeated values

def check(song,artist):

	test1 = cur.execute("SELECT * FROM artist_song WHERE artist_id = (SELECT artist_id FROM artist WHERE artist_name = %s) AND  song_id = (SELECT song_id FROM song WHERE song_name = %s)",(song,artist))
	#print(test1)
	if test1 == 1:
		return True
	else:
		return False

#Here we are doing the webscrapping and creating a 2-d list to pair up the song and artist name. 

def getLinks(articleUrl):
	bsObj = BeautifulSoup(html)
	nameList1 = bsObj.findAll("",{"class":"chart-row__artist"})
	nameList2 = bsObj.findAll("",{"class":"chart-row__song"})
	list1=[]
	list2=[]
	for name in nameList1:
		name = name.get_text()
		name= name.strip()
		#if name not in songs:
		#songs.append(name)
		list1.append(name)
	for name in nameList2:
		name = name.get_text()
		name=name.strip()
		list2.append(name)

	matrix = []
	for i in range(len(list1)):
		matrix.append([list1[i],list2[i]])

	for i in matrix:
		if check(i[0],i[1]) != True:
			store1(i[0],i[1])
	#print(matrix)


	#print(songs)
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
getLinks(html)


cur.close()
conn.close()