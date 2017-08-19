import sqlite3 as sq
import numpy as np
import random as ra
import colorama as co

co.init()
connection = sq.connect('fragen.dat')
baseCursore=connection.cursor()
baseCursore.execute(""" SELECT max(fragennummer) FROM fragen""")
fragenanzahl=baseCursore.fetchall()[0][0]
baseCursore.close()
connection.close()

class User:
    #Variabelen
    listenpunkt=0
    fragenrichtig=0
    anzahlfragen=0
    username=''
    falschefragenliste=[]
    fragenreihnfolge=[]
    fragenreihnfolge_variabel=[]
    #Funktionen


    def name(self,benutzername):
        User.username=benutzername
        connection_user = sq.connect('user.dat')
        userCursor=connection_user.cursor()
        userCursor.execute(""" SELECT COUNT ( fragenrichtig ) FROM user WHERE name = "{}" """.format(User.username))
        userda=userCursor.fetchall()
        if (userda[0][0]==0):
            print('Neuer Benutzer erkannt')
            print('Ein neues Benutzerprofil mit dem Namen ' +'{}'.format(User.username) + ' wird angelegt' )
            userCursor.execute(""" INSERT INTO user VALUES('{}',0,0)""".format(User.username))
            connection_user.commit()
            print('Benuterkonto angelegt')
        else:
            print('Welcome back ' + '{}'.format(User.username))
            print('\n')
            print('Hier deine aktuelle Statistik: ')
            userCursor.execute(""" SELECT fragenrichtig,anzahlfragen FROM user WHERE name = "{}" """.format(User.username))
            statistik=userCursor.fetchall()
            User.anzahlfragen=statistik[0][1]
            User.fragenrichtig=statistik[0][0]
            User.status(self)

        userCursor.close()
        connection_user.close()


    def datenbank(self):
        connection = sq.connect('fragen.dat')
        return connection.cursor()

    def fragenreihnfolge_gesamt(self,anzahlfragen):
         User.fragenreihnfolge=ra.sample(np.arange(1,anzahlfragen+1).tolist(),anzahlfragen)

    def fragenreihnfolge_variabel(self,anzahl):
            User.fragenreihnfolge_variabel=ra.sample(user.fragenreihnfolge,anzahl)

    def fragenreihnfolge_kategorie(self,anzahlfragen,kategorie):
        baseCursor=User.datenbank(self)
        if kategorie=='3' or kategorie == '4':
            baseCursor.execute(""" SELECT   fragennummer  FROM fragen WHERE semester ={} """.format(int(kategorie)))
            duppel=baseCursor.fetchall()
            listederfragen=[i[0]for i in duppel]
            ra.shuffle(listederfragen)
            User.fragenreihnfolge=listederfragen
        elif kategorie =='34':
            User.fragenreihnfolge_gesamt(self,anzahlfragen)
        elif (type(kategorie)== type('a')):
            baseCursor.execute(""" SELECT   fragennummer  FROM fragen WHERE thema ="{}" """.format(kategorie))
            duppel=baseCursor.fetchall()
            listederfragen=[i[0]for i in duppel]
            ra.shuffle(listederfragen)
            User.fragenreihnfolge=listederfragen
        baseCursor.close()
        connection.close()

    def fragenanzahl_kategorie(self,kategorie):
        baseCursor=User.datenbank(self)
        if kategorie=='3' or kategorie == '4':
            baseCursor.execute(""" SELECT   COUNT(fragennummer)  FROM fragen WHERE semester ={} """.format(int(kategorie)))
            anzahl=baseCursor.fetchall()[0][0]
            return anzahl
        elif kategorie =='34':
            baseCursor.execute(""" SELECT max(fragennummer) FROM fragen""")
            anzahl=baseCursor.fetchall()[0][0]
            return anzahl
        elif (type(kategorie)== type('a')):
            baseCursor.execute(""" SELECT   COUNT(fragennummer)  FROM fragen WHERE thema ="{}" """.format(kategorie))
            anzahl=baseCursor.fetchall()[0][0]
            return anzahl
        baseCursor.close()
        connection.close()




    def falschefragen(self):
        User.falschefragenliste.append(User.fragenreihnfolge[User.listenpunkt])

    def falschefragen_varibel(self):
        User.falschefragenliste.append(User.fragenreihnfolge_variabel[User.listenpunkt])


    def status(self):
        print(User.username)
        print('Fragen beantwortet', User.anzahlfragen)
        print('davon richtig', User.fragenrichtig)
        print('\n')

    def save_data(self):
        connection_user = sq.connect('user.dat')
        userCursor=connection_user.cursor()
        userCursor.execute(""" UPDATE user SET fragenrichtig={}, anzahlfragen={} WHERE name="{}" """.format(User.fragenrichtig,User.anzahlfragen,User.username))
        connection_user.commit()
        userCursor.close()
        connection_user.close()


    def fragen_alle(self,fragenanzahl):
        baseCursor=User.datenbank(self)
        for i in range(fragenanzahl):
            User.listenpunkt=i
            n=User.fragenreihnfolge[i]
            baseCursor.execute(""" SELECT frage FROM fragen WHERE fragennummer = {}  """.format(n))
            frage=baseCursor.fetchall()
            print('Frage Nummer:', n)
            print(frage[0][-1])
            input()
            baseCursor.execute(""" SELECT fragenloesung FROM fragen WHERE fragennummer = {}  """.format(n))
            loesung=baseCursor.fetchall()
            print('Loesung:')
            print(loesung[0][-1])
            print('\n')
            print('Hast du die Frage richtig beantwortet? Ja (j) Nein (n)')
            eingabe=input()
            if(eingabe== 'j'):
                User.fragenrichtig+=1
                User.anzahlfragen+=1

            elif(eingabe=='n'):
                User.anzahlfragen+=1
                User.falschefragen(self)
            else:
                print('falsche Eingabe, die fragen wird als falsch gewertet')
                print('\n')
                User.anzahlfragen+=1
                User.falschefragen(self)
        baseCursor.close()
        connection.close()

    def fragen_variabel(self,anzahl):
            baseCursor=User.datenbank(self)
            for i in range(anzahl):
                User.listenpunkt=i
                n=User.fragenreihnfolge_variabel[i]
                baseCursor.execute(""" SELECT frage FROM fragen WHERE fragennummer = {} """.format(n))
                frage=baseCursor.fetchall()
                print('Frage Nummer:', n)
                print(frage[0][-1])
                input()
                baseCursor.execute(""" SELECT fragenloesung FROM fragen WHERE fragennummer = {} """.format(n))
                loesung=baseCursor.fetchall()
                print('Loesung:')
                print(loesung[0][-1])
                print('\n')
                print('Hast du die Frage richtig beantwortet? Ja (j) Nein (n)')
                eingabe=input()
                if(eingabe== 'j'):
                    User.fragenrichtig+=1
                    User.anzahlfragen+=1

                elif(eingabe=='n'):
                    User.anzahlfragen+=1
                    User.falschefragen_varibel(self)
                else:
                    print('falsche Eingabe, die fragen wird als falsch gewertet')
                    print('\n')
                    User.anzahlfragen+=1
                    print(User.listenpunkt)
                    print('\n')
                    User.falschefragen_varibel(self)
            baseCursor.close()
            connection.close()
    def menu(self):
            print('Drittes Semester (3)                   Viertes Semester (4)')
            print('Lagrange-Formalismus (l)               Hamilton-Formalismus (h)')
            print('Kreisel (k)                            Wellen (w)' )
            print('Geometrische Optik (go)                Wellenoptik (wo)' )
            print('Chaostheorie (c)                       Beide Semester (34)')
            print('Grundlagen QM (gq)                     Teilchen im EM-Feld (em)')
            print('Hamonischer Oszi. (ozi)                Spin (s)' )
            print('SymmetrienErhaltugsgrößen (se)         Störungstheorie (st)')
            print('Darstellungen (d)                      Feinstruktur (f)')
            print('Darstellungen (d)                      Identische Teilchen (it)')
            print('\n')
            user_kategorie=input()
            print('Du hast dich für', user_kategorie, 'entschieden')
            anzahl=User.fragenanzahl_kategorie(self,user_kategorie)
            print('In dieser Kategorie gibt es',anzahl, 'Fragen.' )
            print('Möchtest du alle durchgehen ?')
            print('ja (j) oder nein (n)')
            allefragen=input()
            User.fragenreihnfolge_kategorie(self,fragenanzahl,user_kategorie)
            if allefragen == 'n':
                print('Wie viele Fragen möchtest du behandeln ?')
                anzahlfragen=input()
                print('\n')
                User.fragenreihnfolge_variabel(self,int(anzahlfragen))
                User.fragen_variabel(self,int(anzahlfragen))
                User.save_data(self)
            else:
                print('\n')
                anzahlfragen=anzahl
                User.fragen_alle(self,anzahlfragen)
                User.save_data(self)

    def falschefragen_durchgehen(self):
        baseCursor=User.datenbank(self)
        for i in user.falschefragenliste:
            baseCursor.execute(""" SELECT frage FROM fragen WHERE fragennummer = {} """.format(i))
            baseCursor.execute(""" SELECT frage FROM fragen WHERE fragennummer = {} """.format(i))
            frage=baseCursor.fetchall()
            print(frage[0][-1])
            input()
            baseCursor.execute(""" SELECT fragenloesung FROM fragen WHERE fragennummer = {} """.format(i))
            loesung=baseCursor.fetchall()
            print('Loesung:')
            print(loesung[0][-1])
            print('\n')
            print('Hast du die Frage richtig beantwortet? Ja (j) Nein (n)')
            eingabe=input()
            if(eingabe== 'j'):
                User.fragenrichtig+=1
                User.anzahlfragen+=1

            elif(eingabe=='n'):
                User.anzahlfragen+=1
            else:
                print('falsche Eingabe, die fragen wird als falsch gewertet')
                print('\n')
                User.anzahlfragen+=1
            print('\n')
            print('\n')
        baseCursor.close()
        connection.close()



print('Willkomen bei der PHYSIK 3/4 Vorbereitungs Beta')
print('Wie ist dein Name ?')
user_name=input()
user=User()
print('\n')
print('\n')
user.name(user_name)
print( 'Um das Programm nach einer vollständig absolvierten Runde zu beenden, schreibe einfach "exit" ')
print('\n')
print('Jetzt wo du eingeloggt bist, in welchem Themenbereich möchtest du tranieren?')
stopper=''
while stopper!='exit':
    user.menu()
    print('Möchtest du die falschen Fragen nochmal durchgehen und dann weiter machen? (f)')
    print('Nur Weiter machen? (Enter) ')
    print('Möchtest du aufhören? (exit)')
    stopper=input()
    if stopper=='f':
        user.falschefragen_durchgehen()
    elif stopper!='exit':
        stopper=''
