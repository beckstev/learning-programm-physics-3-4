from tkinter import *
from tkinter import ttk
import sqlite3 as sq
import numpy as np
import random as ra

connection = sq.connect('fragen.dat')
baseCursor=connection.cursor()



##### Fragen

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

    def fragenreihnfolge_variabel_f(self,anzahl):
            print('in der Funktion', anzahl)
            User.fragenreihnfolge_variabel=ra.sample(User.fragenreihnfolge,anzahl)

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

    def fragen_variabel(anzahl):
            print('hier war mal eine Funktion')




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
    def menu(self,):
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




#### GUI Funktion

def insert_text(t,window,r,c,h,w): # Set Textbox
    text=Text(window,height=h,width=w)
    text.grid(row=r,column=c)
    text.insert(END,t)

def insert_label(t,window,r,c): # Set Textbox
    label=Label(window,text=t)
    label.grid(row=r,column=c)

def insert_message(t,window,r,c,cspan, rspan):
    var = StringVar()
    message=Message(window,textvariable=var)
    var.set(t)
    message.grid(row=r,column=c, columnspan=cspan,rowspan=rspan)
    return message

def insert_message_text(t,window,r,c,cspan, rspan,w,px,py):
    message=Message(window,text=t,width=w,padx=px,pady=py)
    message.grid(row=r,column=c, columnspan=cspan,rowspan=rspan)
    return message


def insert_entry(window, r,c,cspan,rspan):
    ent=Entry(window)
    ent.grid(row=r,column=c, columnspan=cspan, rowspan=rspan)
    return ent

def insert_entry_int(window, r,c,cspan,rspan):
    ent=IntVar
    ent=Entry(window)
    ent.grid(row=r,column=c, columnspan=cspan, rowspan=rspan)
    return ent

def insert_button(t,window, r,c,cspan,rspan, com):
    button=Button(window,text=t,command=com)
    button.grid(row=r,column=c, columnspan=cspan, rowspan=rspan)
    return button
    print
#### Text Box

#Weclome Page

begruessung_text='Willkommen. \n\n Wähle einen Themenberich aus:\n'
menu_left= '\n Drittes Semester (3)  \n\n Lagrange-Formalismus (l)  \n\n Kreisel (k)  \n\n Geometrische Optik (go) \n \n Chaostheorie (c) \n'
menu_middle=( '\n Viertes Semester (4) \n \n  Hamilton-Formaismus (h)  \n\n Wellen (w) \n \n Wellenoptik (wo)  \n\n  Beide Semester (34) \n' )
menu_middle_right=(' \n Grundlagen QM (gq) \n \n Hamonischer Oszi. (ozi) \n \n Symmetrien/Erhaltugsgrößen (se) \n \n Darstellungen (d) \n\n Wasserstoff (was) \n')
menu_right=('\n Teilchen im EM-Feld (em) \n \n Spin (s) \n \n Störungstheorie (st) \n \n Feinstruktur (f) \n \n Identische Teilchen (it) \n')
eingabe='Wahl:'

#User Choose
opening_text='Pleaser enter your Username?'


## Button fuction


def user_name():
    user.name(user_select.get())
    user_gui.destroy()

def anzahl_fragen():
    user_kategorie=topic_select.get()
    anzahl=user.fragenanzahl_kategorie(user_kategorie)

    ## Anzahl Fragen Gui
    #text
    anzahl_1='In dieser Kategorie gibt es \n      ' + str(anzahl) + '\n \nFragen.'
    anzahl_2= 'Wie viele möchtest du durchgehen?'
    ##
    global number_question
    global number
    #
    number_question=Toplevel(root)
    messegabe_box_1_number_question=insert_message(anzahl_1,number_question,1,1,1,1)
    messegabe_box_1_number_question.configure(padx=10,pady=10)
    messegabe_box_2_number_question=insert_message(anzahl_2,number_question,1,2,1,1)
    messegabe_box_2_number_question.configure(padx=10,pady=10)
    insert_label('Anzahl:',number_question,2,1)
    number=insert_entry(number_question,2,2,1,1)
    insert_button('Go!',number_question,3,3,1,1,show_question)



def show_question():
    global number_of_question
    connection = sq.connect('fragen.dat')
    baseCursor=connection.cursor()
    number_of_question=int(number.get())
    number_question.destroy()
    user.fragenreihnfolge_kategorie(number_of_question,topic_select.get())
    user.fragenreihnfolge_variabel=ra.sample(user.fragenreihnfolge,number_of_question)

    global question_window
    global k
    global antwort_liste
    global fragen_liste
    global frage_box
    global answer_box
    global next_button
    global fragen_number_list

    fragen_liste=[]
    antwort_liste=[]
    fragen_number_list=[]

    k=0


    for i in range(number_of_question):
        User.listenpunkt=i
        User.fragenreihnfolge
        n=user.fragenreihnfolge_variabel[i]
        baseCursor.execute(""" SELECT frage FROM fragen WHERE fragennummer = {} """.format(n))
        frage=baseCursor.fetchall()
        baseCursor.execute(""" SELECT fragenloesung FROM fragen WHERE fragennummer = {} """.format(n))
        loesung=baseCursor.fetchall()
        antwort_liste.append(loesung[0][-1  ])
        fragen_liste.append(frage[0][-1])
        fragen_number_list.append(n)



    question_window=Toplevel(root)
    question_window.title('Physik 3/4 Vorberitungsprogramm ' + ' Fragennummer:  '+ str(fragen_number_list[k]))
    insert_label('Frage:',question_window,0,0)
    insert_label('Antwort', question_window,8,0)
    frage_box=insert_message_text(fragen_liste[k],question_window,0,6,1,1,500,10,30)
    answer_box=insert_message_text('Click Show',question_window,8,6,1,1,500,10,30)
    frage_box.config(font=('ms serif',20))
    answer_box.config(font=('ms serif',20))

    #number_box=insert_message_text('Click Show',question_window,8,6,1,1,500,10,30)

    insert_button('Quit', question_window,9,8,1,1,quit)
    next_button=insert_button('Next', question_window,9,7,1,1,next)
    insert_button('Show', question_window,9,6,1,1,show)

def quit():
    question_window.destroy()
    baseCursor.close()
    connection.close()

def show():
    answer_box.configure(text=antwort_liste[k])

def next():
    global k
    global frage_box
    k=k+1

    if k<number_of_question-1:
        frage_box.configure(text=fragen_liste[k])
        answer_box.configure(text='Click Show')
        question_window.title('Physik 3/4 Vorberitungsprogramm ' + ' Fragennummer:  '+ str(fragen_number_list[k]))
    else:
        frage_box.configure(text=fragen_liste[k])
        answer_box.configure(text='Click Show')
        next_button.destroy()
        insert_button('Quit', question_window,9,8,1,1,quit)
        insert_button('Show', question_window,9,6,1,1,show)






##create User()
user=User()



###Hier lebt die Gui

###### User Gui
root= Tk()


##Gui für User input zur zeit inaktiv
#user_gui=Toplevel(root)
#user_gui.title('User')
#user_name_greeting=insert_message(opening_text,user_gui,1,1,2,1)
#user_name_greeting.configure(width=5000,pady=10)
#insert_label('Name: ',user_gui,2,1)
#user_select=insert_entry(user_gui,2,2,1,1)
#insert_button('Next',user_gui,3,3,1,1,user_name)

 # Main window
#
root.title('Physik 3/4 Vorberitungsprogramm')
greeting=insert_message(begruessung_text,root,1,1,2,1)
greeting.configure(width=5000)
greeting.config(font=('ms serif',15))
#insert_label(menu_left,root,2,1)
menu_middle_mess=insert_message(menu_middle,root,2,2,1,1)
menu_middle_right_mess=insert_message(menu_middle_right,root,2,3,1,1)
menu_right_mess=insert_message(menu_right,root,2,4,1,1)

menu_left_mess=insert_message(menu_left,root,2,1,1,1)
menu_middle_mess.config(font=('ms serif',15))
menu_middle_right_mess.config(font=('ms serif',15))
menu_right_mess.config(font=('ms serif',15))
menu_left_mess.config(font=('ms serif',15))
insert_label(eingabe,root,3,1)
topic_select=insert_entry(root,3,2,1,1)
insert_button('Next',root,3,3,1,1,anzahl_fragen)
root.mainloop()
