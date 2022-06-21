import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS userinfo;')
cur.execute('CREATE TABLE userinfo (id serial PRIMARY KEY,'
                                'email varchar(250) UNIQUE NOT NULL,'
                                 'password varchar(250) NOT NULL,'
                                 'role varchar(250) NOT NULL);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO userinfo (email, password, role)'
            'VALUES (%s, %s, %s)',
            ('admin@gmail.com',
            'abcde',
             'admin')
            )

cur.execute('INSERT INTO userinfo (email, password, role)'
            'VALUES (%s, %s, %s)',
            ('hung@gmail.com',
            'hung',
             'customer')
            )

cur.execute('INSERT INTO userinfo (email, password, role)'
            'VALUES (%s, %s, %s)',
            ('phan@gmail.com',
            'phan',
             'customer')
            )


conn.commit()

cur.close()
conn.close()