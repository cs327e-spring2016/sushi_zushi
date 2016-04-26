
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
import json
import sys

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='', db='billboard')
cur = conn.cursor()

print("Welcome to Billboard Top 100 Data Interface!")
print("")
print("Here are your options:")
print("1. The number of weeks an artist has made the Hot 100 Billboard Chart in 2016.")
print("2. The number of weeks a song has made the Hot 100 Billboard Chart in 2016.")
print("3. The number of songs an artist has had in the top 100 Billboard in 2016.")
print("4. The change in rank a song has had in 2016.")
print("5. The artists that have been the most amount of weeks in the top 100 Billboard in 2016.")
print("6. The songs that have been the most amount of weeks in the top 100 Billboard in 2016.")
print("7. List of songs an artist has had in the Hot 100 Billboard Chart")
print("8. The list of Hottest artists this year")
print("9. Find a song by consulting the given rank and week")
print("10. Exit the interface")


def interact():

    option = input("What would you like to know? ")
    option = int(option)
    while (option > 10) or (option < 0):
        print("Enter a valid option.")
        option = input("What would you like to know? ")
    print("")
    print("")



    if option == 1:

        artist_input = str(input("Enter an artist's name "))
        cur.execute("SELECT artist_id FROM artist WHERE artist_name = %s" , (artist_input))
        artist_id_input = cur.fetchone()
        if not artist_id_input:
            print(artist_input + " hasn't been on the top 100 list this year.")
            cur.close()
            conn.close()
            sys.exit()

        artist_id_input = int(artist_id_input[0])
        cur.execute("SELECT comp_id FROM artist_song WHERE artist_id = %s ", (artist_id_input))
        number = cur.fetchall()
        comp_id_list = []
        for i in number:
            comp_id_list.append(i[0])
        week_list = []
        for i in comp_id_list:
            cur.execute("SELECT (week_id) FROM top100 WHERE (comp_id = %s)",i)
            weeks = cur.fetchall()
            for j in weeks:
                if j not in week_list:
                    week_list.append(j)
        week_list2 = []
        for i in week_list:
            week_list2.append(i[0])

        print(artist_input + " has been on the Hot 100 Chart " + str(len(week_list2)) + " week(s) this year")

    if option ==2:

        song_input = str(input("Enter a song's name "))
        cur.execute("SELECT song_id FROM song WHERE song_name = %s" , (song_input))
        song_id_input = cur.fetchone()
        if not song_id_input:
            print(song_input + " hasn't been on the top 100 list this year.")
            cur.close()
            conn.close()
            sys.exit()

        song_id_input = int(song_id_input[0])
        cur.execute("SELECT comp_id FROM artist_song WHERE song_id = %s ", (song_id_input))
        number = cur.fetchall()
        comp_id_list = []
        for i in number:
            comp_id_list.append(i[0])
        week_list = []
        for i in comp_id_list:
            cur.execute("SELECT (week_id) FROM top100 WHERE (comp_id = %s)",i)
            weeks = cur.fetchall()
            for j in weeks:
                if j not in week_list:
                    week_list.append(j)
        week_list2 = []
        for i in week_list:
            week_list2.append(i[0])

        print(song_input + " has been on the Hot 100 Chart " + str(len(week_list2)) + " week(s) this year")



    if option == 3:

        artist_input = str(input("Enter an artist name "))
        cur.execute("SELECT artist_id FROM artist WHERE artist_name = %s" , (artist_input))
        artist_id_input = cur.fetchone()
        if not artist_id_input:
            print(artist_input + " hasn't been on the top 100 list this year.")
            cur.close()
            conn.close()
            sys.exit()
        artist_id_input = int(artist_id_input[0])
        cur.execute("SELECT comp_id FROM artist_song WHERE artist_id = %s ", (artist_id_input))
        comp_ids = cur.fetchall()
        amount_songs = len(comp_ids)
        print(artist_input + " has had " + str(amount_songs) + " song(s) in the top 100 this year.")

    if option == 4:
        song_input = str(input("Enter a song's name "))
        cur.execute("SELECT song_id FROM song WHERE song_name = %s", (song_input))
        song_id_input = cur.fetchone()
        if not song_id_input:
            print(song_input + " hasn't been on the top 100 list this year.")
            cur.close()
            conn.close()
            sys.exit()
        song_id_input = song_id_input[0]
        cur.execute("SELECT comp_id FROM artist_song WHERE song_id = %s", (song_id_input))
        comp_id_input = cur.fetchone()
        comp_id_input = comp_id_input[0]
        cur.execute("SELECT MAX(rank) FROM top100 WHERE comp_id = %s", (comp_id_input))
        worst_rank = cur.fetchone()[0]
        cur.execute("SELECT MIN(rank)FROM top100 WHERE comp_id = %s", (comp_id_input))
        best_rank = cur.fetchone()[0]
        cur.execute("SELECT week_id FROM top100 WHERE (rank = %s) AND (comp_id = %s)", (best_rank,comp_id_input))
        best_week = cur.fetchone()[0]
        cur.execute("SELECT week_id FROM top100 WHERE (rank = %s) AND (comp_id = %s)", (worst_rank, comp_id_input))
        worst_week = cur.fetchone()[0]
        print("The song " + song_input + " had its worst week on Billboard 100 on week " + str(worst_week) + " with rank: " + str(worst_rank))
        print("It had its best week on week " + str(best_week) + " with rank: " + str(best_rank))

    if option == 5:
        #First we need to create a table in which the artist name, the 
        artist_week =cur.execute("SELECT * FROM (SELECT b.artist_name, COUNT(b.artist_name)  AS number FROM (SELECT DISTINCT a.artist_name, t.week_id FROM artist a INNER JOIN artist_song ab  ON a.artist_id = ab.artist_id INNER JOIN top100 t ON ab.comp_id = t.comp_id ) b  GROUP BY b.artist_name ) c WHERE c.number =17;")
        artist_week= cur.fetchall()
        for i in artist_week:
            print(i[0])

        print("These artists have been in the HOT100 Billboard Charts for 17 weeks in 2016")

    if option == 6:

        song_week = cur.execute("SELECT * FROM (SELECT b.song_name, COUNT(b.song_name)  AS number FROM (SELECT DISTINCT a.song_name, t.week_id FROM song a INNER JOIN artist_song ab  ON a.song_id = ab.song_id INNER JOIN top100 t ON ab.comp_id = t.comp_id ) b  GROUP BY b.song_name ) c WHERE c.number =17;")
        song_week = cur.fetchall()
        for i in song_week:
            print(i[0])
        print("These songs have been in the HOT100 Bibllboard Charts for 17 weeks in 2016")

    if option == 7:

        artist_input = str(input("Enter an artist's name "))
        cur.execute("SELECT artist_id FROM artist WHERE artist_name = %s" , (artist_input))
        artist_id_input = cur.fetchone()
        if not artist_id_input:
            print(artist_input + " hasn't been on the HOT 100 list this year.")
            cur.close()
            conn.close()
            sys.exit()

        cur.execute("SELECT song_name FROM song INNER JOIN artist_song ON song.song_id = artist_song.song_id WHERE artist_id = %s", (artist_id_input))
        print("The following songs by " + artist_input + " have been on the HOT 100 Billboard this year: ")
        for i in cur.fetchall():
            print(i[0])
            
    if option == 8:

        cur.execute("SELECT artist_id, COUNT(artist_id) count FROM artist_song INNER JOIN top100 ON artist_song.comp_id = top100.comp_id GROUP BY artist_id ORDER BY count DESC;")
        print("Here are the 10 hottest artists this year: ")
        artists = list(cur.fetchall()[0:10])
        index = - 1
        for i in artists:
            index += 1
            artists[index] = list(i)
            cur.execute("SELECT artist_name FROM artist WHERE artist_id = %s",i[0])
            artists[index][0] = cur.fetchone()[0]
            
        for i in artists:
            print(str(i[0]) + " has appeared " + str(i[1]) + " distinct times in the HOT 100 this year.")

    if option == 9:

        rank_input = eval(input("Enter a rank: "))
        week_input = eval(input("Enter a week: "))
        while (rank_input > 100) or (rank_input < 0) or (week_input > 17) or (week_input <0):
            print("Please enter valid rank and input.")
            rank_input = eval(input("Enter a rank: "))
            week_input = eval(input("Enter a week: "))

        cur.execute("SELECT week_date FROM week WHERE week_id = %s", week_input)
        week_name = cur.fetchone()[0]
        cur.execute("SELECT comp_id FROM top100 WHERE (rank = %s) AND (week_id = %s)",(rank_input,week_input))
        comp_id_input = cur.fetchone()[0]
        cur.execute("SELECT artist_name, song_name FROM artist_song INNER JOIN song ON artist_song.song_id = song.song_id INNER JOIN artist ON artist_song.artist_id = artist.artist_id  WHERE comp_id = %s;", comp_id_input)
        result = cur.fetchone()
        song_name = result[1]
        artist_name = result[0]
        print("On the week of " + str(week_name) + ", the song with rank " + str(rank_input) + " was " + str(song_name) + " by " + str(artist_name))

    if option == 10:
        print("Goobye!")
        cur.close()
        conn.close()
        sys.exit()
        

    return option

def main():
    interact()
    while interact() != 10:
        interact()
    cur.close()
    conn.close()

main()






