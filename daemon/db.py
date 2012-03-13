import os
import sqlite3

# Setup database
db_fn = os.path.join(*(list(os.path.split(os.path.abspath(__file__))[:-1])+[".dc.db"]))
db = sqlite3.connect(db_fn)
cursor = db.cursor()

# Create the tables
cursor.execute("""create table if not exists apps
    (id integer primary key, app text unique)""")
cursor.execute("""create table if not exists app_usage
    (id integer primary key, app_id integer, year integer, month integer,
    day integer, weekday integer, time real)""")
cursor.execute("""create table if not exists urls
    (url text primary key, num integer default 0)""")
cursor.execute("""create table if not exists docs
    (id integer primary key, ext text, year integer, month integer,
    day integer, weekday integer, time real)""")
db.commit()
cursor.close()

