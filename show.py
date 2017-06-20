import sqlite3 as sq
import random as ra
import pandas as pd
import numpy as np
connection = sq.connect('fragen.dat')
baseCursor=connection.cursor()
frage_l=[]
loesung_l=[]
nummer=[]
baseCursor.execute(""" SELECT max(fragennummer) FROM fragen""")
anzahl_max=baseCursor.fetchall()
for n in range(anzahl_max[0][0]+1):
    baseCursor.execute(""" SELECT frage FROM fragen WHERE fragennummer={}""".format(n))
    frage=baseCursor.fetchall()
    baseCursor.execute(""" SELECT fragenloesung FROM fragen WHERE fragennummer = {} """.format(n))
    loesung=baseCursor.fetchall()

    #zusammen=str(n)+ '      ' +str(frage)+ '      ' + str(loesung)
    #frage_l.append(zusammen)
    #baseCursor.execute(""" SELECT * FROM fragen WHERE fragennummer={}""".format(n))

    print('Fragennummer', n)
    print('Frage \n', frage)
    print('loesung \n', loesung)
    print('\n')
    frage_l.append(frage)
    loesung_l.append(loesung)
    nummer.append(n)
baseCursor.close()
connection.close()

#thefile = open('frage_loesung.txt', 'w')
#for item in frage_l:
#    thefile.write("%s\n" % item)
