#Here we are importing the programs we need and connecting to mysql 

from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import pymysql
import json
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='', db='billboard')
cur = conn.cursor()
#cur.execute("USE ")

#Here we are storing the values we fetched to mysql
def store1(rank,artist_name2,song_name2):

	#cur.execute("INSERT INTO song (song_amount, song_name) VALUES ((\"%s\",\"%s\")", (song_id, song_name)) 
	#t = (song_id2, song_name2)
	#cur.execute("""INSERT INTO artist_song (name_artist,name_song) VALUES({1})""".format(json.dumps(artist_name2,song_name2)))
	cur.execute("INSERT INTO top100 (week_id, rank, comp_id) VALUES ((SELECT week_id FROM week WHERE week_id= 17 ), (%s), (SELECT comp_id FROM artist_song WHERE artist_id = (SELECT artist_id FROM artist WHERE artist_name = %s) AND song_id = (SELECT song_id FROM song WHERE song_name = %s)))",(rank,artist_name2,song_name2))
	cur.connection.commit()
#This function helps to order our table.
def order():
	cur.execute("SELECT * FROM top100 ORDER BY week_id,rank")
	cur.connection.commit()

#Here we are doing our webscrapping and again creating a 2-d list to export our values as paired.
def getLinks(articleUrl):
	bsObj = BeautifulSoup(html)
	nameList1 = bsObj.findAll("",{"class":"chart-row__artist"})
	nameList2 = bsObj.findAll("",{"class":"chart-row__song"})
	rank = bsObj.findAll("",{"class":"chart-row__current-week"})
	list1=[]
	list2=[]
	list3=[]
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

	for number in rank:
		number = number.get_text()
		number=number.strip()
		list3.append(number)

	matrix = []
	for i in range(len(list1)):
		matrix.append([list3[i],list1[i],list2[i]])

	for i in matrix:
			store1(i[0],i[1],i[2])
	#print(matrix)


	#print(songs)
#Here are the different URL's we used four our dates.

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
#order()



cur.close()
conn.close()
