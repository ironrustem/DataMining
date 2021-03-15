import vk_api

import psycopg2
from psycopg2 import sql

con = psycopg2.connect(host='database-course.cuh9nfz6hd2g.us-east-1.rds.amazonaws.com',
                       port='5432', user='postgres', password='BoskaData')

vk_session = vk_api.VkApi(token="ad3741635a3e27742a193267f4d82b753a16d0d61cb966cd3f103b77b1cff1c0ec12f3457b4278f520e60")

vk = vk_session.get_api()
walls = vk.wall.get(domain='itis_kfu', count=20)

un_words = {}

for wall in walls['items']:
    words = wall['text'].split(' ')
    for j in words:
        j = j.strip()
        words3 = j.split('\n')
        for word in words3:
            words3 = word.split(' ')
            for i1 in words3:
                if i1 != "":
                    marks = [')', '(', '\n', '•', ',', ';', '•', '*', '%', '₽', '$', '/', '-', '.', '!', '—', '\"',
                             '\'', '@',
                             '^', ':', '»', '«', '◾', '“']
                    for i2 in marks:
                        i1 = i1.strip(i2)
                    if i1 != "":
                        if i1 in un_words.keys():
                            un_words[str(i1)] = un_words.get(str(i1)) + 1
                        else:
                            un_words[str(i1)] = 1

with con.cursor() as cursor:
    i = 0
    cursor.execute(f'''TRUNCATE TABLE  topwords;''')
    for w in sorted(un_words, key=un_words.get, reverse=True):
        if i >= 100:
            break
        cursor.execute(f'''INSERT INTO topwords (word, count) VALUES('{w}',{un_words[w]});''')
        i += 1

con.commit()
con.close()