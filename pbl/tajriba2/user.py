from tkinter import *


# def create_table(self):
#         if db_connection.is_connected() == False:
#           db_connection.connect()
#         db_cursor.execute("CREATE DATABASE IF NOT EXISTS Bemor")  
#         db_cursor.execute("use Bemor")  
#         db_cursor.execute("create table if not exists users(Id INT(10) NOT NULL  PRIMARY KEY AUTO_INCREMENT,login VARCHAR(30), parol VARCHAR(30))AUTO_INCREMENT=1")
#         db_connection.commit()


root = Tk()
root.title("Login UI using Pack")
root.geometry("400x320")  # set starting size of window
root.maxsize(400, 320)  # width x height
root.config(bg="#6FAFE7")  # set background color of root window

login = Label(root, text="Enter admin name", bg="#2176C1", fg='white', relief=RAISED)
login.pack(ipady=5, fill='x',pady=(0,30))
login.config(font=("Font", 30))  # change font and size of label


# Username Entry
username_frame = Frame(root, bg="#6FAFE7")
username_frame.pack()

res = Label(username_frame, text="Username", bg="#6FAFE7").pack(side='left', pady=7)

## Connecting to the database

## importing 'mysql.connector' for connection to mysql database
import mysql.connector

## connecting to the database using 'connect()' method
## it takes 3 required parameters 'host', 'user', 'password'
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="")
# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor(buffered=True)  # "buffered=True".makes db_cursor.row_count return actual number of records selected otherwise would return -1


def checkInput():
    '''check that the username and password match'''
    if db_connection.is_connected() == False:
        db_connection.connect()
    db_cursor.execute("use Bemor")  # Interact with yordamch Database
    rollno  = 0

    entered_usernm = username_entry.get()  # get username from Entry widget
    entered_pswrd = password_entry.get()  # get password from Entry widget

    # xato tog'rilikga tekshirish
    query1 = f"SELECT count(*) as soni FROM users where login='{entered_usernm}' and parol='{entered_pswrd}'"
    # implement query Sentence
    db_cursor.execute(query1)  # Retrieving maximum yordamch id no

    row = db_cursor.fetchone()
    if row[0]==1:
        print("Hello!")
        
        root.destroy()  #2 chi oynani yopish
        #2chi oynaga otish
        from subprocess import call
        call("python C:\\Users\\user\\Desktop\\pbl\\tajriba2\\bemor.py")
        login.configure(text="Hello.")
    else:
        login.configure(text="Xato.")

def toggled():
    '''display a message to the terminal every time the check button
    is clicked'''
    print("The check button works.")


Label(username_frame, text="Username", bg="#6FAFE7").pack(side='left', pady=7)

username_entry = Entry(username_frame, bd=3)
username_entry.pack(side='right')

# Password entry
password_frame = Frame(root, bg="#6FAFE7")
password_frame.pack()

Label(password_frame, text="Password", bg="#6FAFE7").pack(side='left', pady=7)

password_entry = Entry(password_frame, bd=3)
password_entry.pack(side='right')

# Create Go! Button

go_button = Button(root, text="GO!", command=checkInput, bg="#6FAFE7", width=15)

go_button.pack(pady=(20,30))



root.mainloop()