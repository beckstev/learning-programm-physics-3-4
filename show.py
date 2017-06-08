import sqlite3 as sq
import random as ra

connection = sq.connect('fragen.dat')
baseCursor=connection.cursor()

baseCursor.execute(""" SELECT max(fragennummer) FROM fragen""")
anzahl_max=baseCursor.fetchall()
for n in range(anzahl_max[0][0]+1):
    baseCursor.execute(""" SELECT frage FROM fragen WHERE fragennummer={}""".format(n))
    frage=baseCursor.fetchall()
    baseCursor.execute(""" SELECT fragenloesung FROM fragen WHERE fragennummer={}""".format(n))
    antwort=baseCursor.fetchall()

    #baseCursor.execute(""" SELECT * FROM fragen WHERE fragennummer={}""".format(n))
    print('Fragennummer', n)
    print('Frage \n', frage)
    print('Antwort \n', antwort)
    print('\n')

baseCursor.close()
connection.close()
