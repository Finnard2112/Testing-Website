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
                                 'email varchar (254) UNIQUE,'
                                 'password varchar (50) NOT NULL,'
                                 'date_created date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO userinfo (email, password)'
            'VALUES (%s, %s)',
            ('admin@gmail.com',
             'abcde')
            )


conn.commit()

cur.close()
conn.close()