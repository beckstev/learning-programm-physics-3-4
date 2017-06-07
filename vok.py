
import sqlite3 as sq
import random as ra

connection = sq.connect('fragen.dat')
baseCursor=connection.cursor()
#baseCursor.execute(""" CREATE TABLE fragen(fragennummer SMALLINT PRIMARY KEY,semester SMALLINT, thema TEXT NOT NULL,frage TEXT NOT NULL, fragenloesung TEXT NOT NULL)""")
#baseCursor.execute("""INSERT INTO fragen VALUES(1,3, 'l',"Wodurch zeichnen sich virtuelle Verrückungen aus", "1. Instantant, 2. Berücksichtigen die ZWangsbedingungen, 3. infinitesimal")""")
#baseCursor.execute("""INSERT INTO fragen VALUES(2,3,'h',"Wie kommt man von Lagrange zu Hamilton ?", "Legendre-Tafo")""")
#baseCursor.execute("""INSERT INTO fragen VALUES(3,3,'k',"Wo hat man ein permanentes äußeres Drehmoment?", "praezession")""")
#baseCursor.execute(""" UPDATE fragen SET thema="wo" WHERE frage ="Was besagt das Babinetsche Prinzip?"  """)
#connection.commit()


#baseCursor.execute(""" SELECT * FROM fragen""")
#fragen=baseCursor.fetchall()
#print(fragen)
stopper=''
baseCursor.execute(""" SELECT max(fragennummer) FROM fragen""")
startzahl=baseCursor.fetchall()[0][0]

while stopper != 'x':
    startzahl+=1
    print('Frage ?')
    frage=input()
    print('Lösung?')
    loesung=input()
    print('Semester?')
    semester=input()
    print('thema')
    thema=input()
    baseCursor.execute("""INSERT INTO fragen VALUES({},{},"{}","{}", "{}")""".format(startzahl,int(semester),thema,frage,loesung))
    connection.commit()
    stopper=input()

#print(letzte_element)
#print(test)
baseCursor.close()
connection.close()
