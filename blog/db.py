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
cur.execute('DROP TABLE IF EXISTS tests_registration;')
cur.execute('CREATE TABLE tests_registration (id serial PRIMARY KEY,'
                                'email varchar(250) NOT NULL,'
                                 'startDate timestamp NOT NULL,'
                                 'endDate timestamp NOT NULL);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO tests_registration (email, startDate, endDate)'
            'VALUES (%s, %s, %s)',
            ('admin@gmail.com',
            '14-Jun-2022 2:51 PM',
             '15-Jun-2022 2:51 PM')
            )


conn.commit()

cur.close()
conn.close()