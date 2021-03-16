import vk_api
import psycopg2
import sys


def words(passwordDataBase, tokenVK):
    con = psycopg2.connect(host='database-course.cuh9nfz6hd2g.us-east-1.rds.amazonaws.com',
                           port='5432', user='postgres', password=passwordDataBase)

    vk_session = vk_api.VkApi(token=tokenVK)
    vk = vk_session.get_api()

    walls1 = vk.wall.get(domain='itis_kfu', count=100)
    walls2 = vk.wall.get(domain='itis_kfu', count=100, offset=100)

    def sortWall(walls, un_words1):
        if not un_words1:
            un_words1 = {}
        un_words = un_words1
        for wall in walls['items']:
            words = wall['text'].split(' ')
            for j in words:
                j = j.strip()
                words3 = j.split('\n')
                for word in words3:
                    words3 = word.split(' ')
                    for i1 in words3:
                        if i1 != "":
                            marks = [')', '(', '\n', '•', ',', ';', '•', '*', '%', '₽', '$', '/', '-', '.', '!', '—',
                                     '\"',
                                     '\'', '@',
                                     '^', ':', '»', '«', '◾', '“']
                            for i2 in marks:
                                i1 = i1.strip(i2)
                            if i1 != "":
                                i2 = i1.lower()
                                if i2 in un_words.keys():
                                    un_words[str(i2)] = un_words.get(str(i2)) + 1
                                else:
                                    un_words[str(i2)] = 1
        return un_words

    un_wordsR = sortWall(walls1, {})
    un_wordsR = sortWall(walls2, un_wordsR)

    leng = len(un_wordsR)
    with con.cursor() as cursor:
        i = 0
        cursor.execute(f'''TRUNCATE TABLE  topwords;''')

        for w in un_wordsR:
            print(f'\r записывается {i + 1} из {leng}', end="", flush=True)
            cursor.execute(f'''INSERT INTO topwords (word, count) VALUES('{w}',{un_wordsR[w]});''')
            i += 1

    con.commit()
    con.close()


if len(sys.argv) == 3:
    words(sys.argv[1], sys.argv[2])
else:
    print("Print with me passwordDataBase and tokenVK")
