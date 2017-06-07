import sqlite3 as sq


connection_user = sq.connect('user.dat')
userCursor=connection_user.cursor()
userCursor.execute(""" CREATE TABLE user(name TEXT NOT NULL PRIMARY KEY, fragenrichtig SMALLINT NOT NULL ,anzahlfragen SMALLINT NOT NULL)""")

userCursor.close()
connection_user.close()
