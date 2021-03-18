import requests
import vk_api
import psycopg2

import airflow
from airflow import DAG
import datetime
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

vk = vk_api.VkApi().get_api()
con = psycopg2


def connect(tokenVK, passwordDataBase):
    connectVk(tokenVK)
    connectBD(passwordDataBase)


def topWords():
    un_wordsR = get_data(vk)
    save_data(un_wordsR, con)


def connectVk(tokenVK1):
    vk_session = vk_api.VkApi(token=tokenVK1)
    global vk
    vk = vk_session.get_api()



def connectBD(passwordDataBase1):
    global con
    con = psycopg2.connect(host='database-course.cuh9nfz6hd2g.us-east-1.rds.amazonaws.com',
                           port='5432', user='postgres', password=passwordDataBase1)

def get_data(vk):
    walls1 = vk.wall.get(domain='itis_kfu', count=100)
    walls2 = vk.wall.get(domain='itis_kfu', count=100, offset=100)
    return validate_data(walls1, walls2)


def validate_data(walls1, walls2):
    un_wordsR = parse_data(walls1, {})
    un_wordsR = parse_data(walls2, un_wordsR)
    return un_wordsR


def parse_data(walls, un_words1):
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


def save_data(un_wordsR, con):
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


def main():
    topWords()


def connect1():
    connect('ad3741635a3e27742a193267f4d82b753a16d0d61cb966cd3f103b77b1cff1c0ec12f3457b4278f520e60', 'BoskaData')


args = {
    'owner': 'airflow',
    'start_date': datetime.datetime(2021, 3, 18),
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=2),
    'depends_on_past': False,
}

with DAG(dag_id='topWords', default_args=args, schedule_interval=None) as dag:
    get_connect = PythonOperator(
        task_id='connectVKAndBD',
        python_callable=connect1,
        dag=dag
    )
    parse_vk_itis = PythonOperator(
        task_id='topWordsVk',
        python_callable=main,
        dag=dag
    )

