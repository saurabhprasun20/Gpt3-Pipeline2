import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='julidata',
    user='uzh_admin',
    password='password'
)

cur = conn.cursor()

cur.execute('INSERT INTO davinci_avg (question, answer, response_time)'
            'values (%s, %s, %s)',
            ('This is question again', 'this is answer agAain', 1010112))

cur.execute('truncate davinci_avg')

conn.commit()
cur.close()
conn.close()