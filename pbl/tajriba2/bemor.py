from tkcalendar import Calendar, DateEntry
import tkinter as tk
import tkinter.messagebox as mb
import tkinter.ttk as ttk
from datetime import datetime
import os
import sys

from tkinter import *


import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="")
db_cursor = db_connection.cursor(buffered=True) 

class BemorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bemor ma'lumotlari")
        self.geometry("800x650+351+174")
        self.lblTitle = tk.Label(self, text="Bemor ma'lumotlari", font=("Helvetica", 16), bg="yellow", fg="green")
        self.lblmfamilya = tk.Label(self, text="Familya:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblmismi= tk.Label(self, text="Ismi:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblContactNo = tk.Label(self, text="Telefon raqam:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblpasport = tk.Label(self, text="Pasport seriyasi:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblDOB = tk.Label(self, text="Tug'ilgan kuni:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblSelect = tk.Label(self, text="O'chirish yoki o'zgartirish uchun tanlang", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblSearch = tk.Label(self, text="ID tanlang:",font=("Helvetica", 10), bg="blue", fg="yellow")

        self.entmfamilya = tk.Entry(self)
        self.entmismi = tk.Entry(self)
        self.entContact = tk.Entry(self)
        self.entpasport = tk.Entry(self)
        self.calDOB = DateEntry(self, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=1950,locale='en_US', date_pattern='y-mm-dd')
        #self.entDOB = tk.Entry(self)
        self.entSearch = tk.Entry(self)


        self.btn_register = tk.Button(self, text="Ma'lumot qo'shish", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=self.register_Bemor)
        self.btn_update = tk.Button(self,text="O'zgartirish",font=("Helvetica",11),bg="yellow", fg="blue",command=self.update_Bemor_data)
        self.btn_delete = tk.Button(self, text="O'chirish", font=("Helvetica", 11), bg="yellow", fg="blue",
                                    command=self.delete_Bemor_data)
        self.btn_clear = tk.Button(self, text="Oynani tozalash", font=("Helvetica", 11), bg="yellow", fg="blue",
                                    command=self.clear_form)
        self.btn_show_all = tk.Button(self, text="Hammasini korish", font=("Helvetica", 11), bg="yellow", fg="blue",
                                   command=self.load_Bemor_data)
        self.btn_search = tk.Button(self, text="Qidirish", font=("Helvetica", 11), bg="yellow", fg="blue",
                                   command=self.show_search_record)
        self.btn_exit = tk.Button(self, text="Chiqish", font=("Helvetica", 16), bg="yellow", fg="blue",command=self.exit)
       
       #anketaga otish button
        self.btn_open = tk.Button(self,text="Anketaga o'tish",font=("Helvetica",11),bg="yellow", fg="blue",command=lambda:self.open("anketa.py")).pack()

        columns = ("#1", "#2", "#3", "#4", "#5", "#6")
        self.tvBemor= ttk.Treeview(self,show="headings",height="5", columns=columns)
        self.tvBemor.heading('#1', text='ID', anchor='center')
        self.tvBemor.column('#1', width=60, anchor='center', stretch=False)
        self.tvBemor.heading('#2', text='Familya', anchor='center')
        self.tvBemor.column('#2', width=10, anchor='center', stretch=True)
        self.tvBemor.heading('#3', text='Ismi', anchor='center')
        self.tvBemor.column('#3',width=10, anchor='center', stretch=True)
        self.tvBemor.heading('#4', text='Pasport', anchor='center')
        self.tvBemor.column('#4',width=10, anchor='center', stretch=True)
        self.tvBemor.heading('#5', text='Telefon raqam', anchor='center')
        self.tvBemor.column('#5', width=10, anchor='center', stretch=True)
        self.tvBemor.heading('#6', text="Tug'ilgan kuni", anchor='center')
        self.tvBemor.column('#6', width=10, anchor='center', stretch=True)

        #Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget
        vsb= ttk.Scrollbar(self, orient=tk.VERTICAL,command=self.tvBemor.yview)
        vsb.place(x=40 + 640 + 1, y=310, height=180 + 20)
        self.tvBemor.configure(yscroll=vsb.set)
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tvBemor.xview)
        hsb.place(x=40 , y=310+200+1, width=620 + 20)
        self.tvBemor.configure(xscroll=hsb.set)
        self.tvBemor.bind("<<TreeviewSelect>>", self.show_selected_record)

        self.lblTitle.place(x=280, y=30,  height=27, width=300)
        self.lblmfamilya.place(x=125, y=70,  height=23, width=150)       #kenglik
        self.lblmismi.place(x=125, y=100,  height=23, width=150)
        self.lblContactNo.place(x=125, y=129,  height=23, width=150)
        self.lblpasport.place(x=125, y=187,  height=23, width=150)
        self.lblDOB.place(x=125, y=158, height=23, width=150)
        self.lblSelect.place(x=150, y=280, height=23, width=400)
        self.lblSearch.place(x=174, y=560, height=23, width=134)
        self.entmfamilya.place(x=277, y=72, height=21, width=186)
        self.entmismi.place(x=277, y=100, height=21, width=186)
        self.entContact.place(x=277, y=129, height=21, width=186)
        self.entpasport.place(x=278, y=188, height=21, width=186) 

        self.calDOB.place(x=277, y=158, height=21, width=186)

        self.entSearch.place(x=310, y=560, height=21, width=186)
        self.btn_register.place(x=90, y=245, height=25, width=125)
        self.btn_update.place(x=230, y=245, height=25, width=90)
        self.btn_delete.place(x=335, y=245, height=25, width=75)
        self.btn_clear.place(x=425, y=245, height=25, width=125)
        self.btn_show_all.place(x=565, y=245, height=25, width=126)
        self.btn_search.place(x=498, y=558, height=26, width=60)
        self.btn_exit.place(x=320, y=610,  height=31, width=80)
        self.tvBemor.place(x=40, y=310, height=200, width=640)
        self.create_table()
        self.load_Bemor_data()

    def clear_form(self):
      self.entmfamilya.delete(0, tk.END)
      self.entmismi.delete(0, tk.END)
      self.entContact.delete(0, tk.END)
      self.entpasport.delete(0, tk.END)
      self.calDOB.delete(0, tk.END)



    def exit(self):
      MsgBox = mb.askquestion('Exit Application', 'Are you sure you want to exit the application', icon='warning')
      if MsgBox == 'yes':
        self.destroy()

    
    #anketaga otishi
   
    def open(self, filename):
       os.chdir(os.getcwd())
       os.system('python '+filename+" --id "+str(ID))


    def delete_Bemor_data(self):
      MsgBox = mb.askquestion("O'chirish", "Ma'lumotlar o'chirilsinmi", icon='warning')
      if MsgBox == 'yes':
          if db_connection.is_connected() == False:
              db_connection.connect()
          db_cursor.execute("use Bemor")  # Interact with Student Database
          # deleteing selected student record
          Delete = "delete from Bemor where ID='%s'" % (ID)
          db_cursor.execute(Delete)
          db_connection.commit()
          mb.showinfo("O'chirildi", "Bemor ma'kumotlari o'chirildi")
          self.load_Bemor_data()
          self.entmfamilya.delete(0, tk.END)
          self.entmismi.delete(0, tk.END)
          self.entContact .delete(0, tk.END)
          self.entpasport.delete(0, tk.END)
          self.calDOB.delete(0, tk.END)




    def create_table(self):
        if db_connection.is_connected() == False:
          db_connection.connect()
        db_cursor.execute("CREATE DATABASE IF NOT EXISTS Bemor")  
        db_cursor.execute("use Bemor")  
        db_cursor.execute("create table if not exists Bemor(Id INT(10) NOT NULL  PRIMARY KEY AUTO_INCREMENT,mfamilya VARCHAR(30),mismi VARCHAR(30),pasport VARCHAR(30),mobileno VARCHAR(10),dob date)AUTO_INCREMENT=1")
        db_connection.commit()

    def register_Bemor(self):
        if db_connection.is_connected() == False:
          db_connection.connect()
        mfamilya = self.entmfamilya.get()  
        mismi = self.entmismi.get()  
        contact_no = self.entContact.get() 
        pasport = self.entpasport.get()  
        dob = self.calDOB.get()  
        if mfamilya == "":
            mb.showinfo('Information', "Bemor familyasini kiriting")
            self.entmfamilya.focus_set()
            return
        if mismi == "":
            mb.showinfo('Information', "Bemor ismi kiriting")
            self.entmismi.focus_set()
            return
        if contact_no == "":
            mb.showinfo('Information', "Bemor telefon raqamini kiriting")
            self.entContact.focus_set()
            return
        if dob == "":
            mb.showinfo('Information', "Bemor tug'ilgan kunini kiriting")
            self.calDOB.focus_set()
            return
        if pasport == "":
            mb.showinfo('Information', "Bemor pasport seriyasini kiriting")
            self.entpasport.focus_set()
            return
       

        try:
            ID =int(self.fetch_max_ID())
            print("New Bemor Id: " + str(ID))
            query2 = "INSERT INTO Bemor (ID, mfamilya,mismi,pasport,mobileno,dob) VALUES (%s, %s,%s, %s,%s, %s)"

            db_cursor.execute(query2, (ID, mfamilya, mismi, pasport, contact_no,dob))
            mb.showinfo('Information', "Bemor ma'lumotlari qo'shildi")
            db_connection.commit()
            self.load_Bemor_data()
        except mysql.connector.Error as err:
            print(err)
            db_connection.rollback()
            mb.showinfo('Information', "Bemor ma'lumotlarini qo'shishda xatolik!!!")
        finally:
           db_connection.close()

    def fetch_max_ID(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        db_cursor.execute("use Bemor")  
        ID  = 0
        query1 = "SELECT ID FROM Bemor order by  id DESC LIMIT 1"

        db_cursor.execute(query1)
        print("No of Record Fetched:" + str(db_cursor.rowcount))
        if db_cursor.rowcount == 0:
            ID = 1
        else:
            rows = db_cursor.fetchall()
            for row in rows:
                ID = row[0]
            ID = ID + 1
        print("Max Student Id: " + str(ID))
        return ID

    def show_search_record(self):

        if db_connection.is_connected() == False:
            db_connection.connect()
        s_ID = self.entSearch.get()  
        print(s_ID)
        if  s_ID == "":
            mb.showinfo('Information', "Bemor IDsini bosing")
            self.entSearch.focus_set()
            return
        self.tvBemor.delete(*self.tvBemor.get_children()) 
        db_cursor.execute("use Bemor")  
        sql = "SELECT ID,mfamilya,mismi,pasport,mobileno,date_format(dob,'%d-%m-%Y') FROM Bemor where mfamilya like '%" + s_ID + "%' or mismi like '%" + s_ID + "%' or pasport like '%" + s_ID + "%' or mobileno like '%" + s_ID + "%'"
        # bazaga bor yoqligini tekshirish chala
        # sql = "Select count(*) end sano "
        db_cursor.execute(sql)
        total = db_cursor.rowcount
        #if total ==0:
            #mb.showinfo("Info", "Nothing To Display,Please add data")
            #return
        print("Total Data Entries:" + str(total))
        rows = db_cursor.fetchall()

        ID = ""
        Bemor_Familya = ""
        Bemor_Ismi = ""
        pasport = ""
        Phone_Number = ""
        DOB =""
        for row in rows:
            ID = row[0]
            Bemor_Familya = row[1]
            Bemor_Ismi = row[2]
            pasport = row[3]
            Phone_Number = row[4]
            DOB = row[5]
            ddd =  datetime.strptime(DOB, "%d-%m-%Y").date()
            DOB = ddd.strftime('%Y-%m-%d')
            self.tvBemor.insert("", 'end', text=ID, values=(ID, Bemor_Familya, Bemor_Ismi, pasport, Phone_Number,DOB))


    def show_selected_record(self, event):
        self.clear_form()
        for selection in self.tvBemor.selection():
            item = self.tvBemor.item(selection)
        global ID
        ID,Bemor_Familya,Bemor_Ismi,pasport,contact_no,dob = item["values"][0:7]
        self.entmfamilya.insert(0, Bemor_Familya)
        self.entmismi.insert(0, Bemor_Ismi)
        self.entpasport .insert(0, pasport)
        self.entContact.insert(0, contact_no)
        self.calDOB.insert(0, dob)
        return ID

    def update_Bemor_data(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        print("O'zgardi")
        db_cursor.execute("use Bemor")  
        Bemor_Familya = self.entmfamilya.get()
        Bemor_Ismi = self.entmismi.get()
        Phone_Number = self.entContact.get()
        pasport = self.entpasport.get()
        DOB = self.calDOB.get()
        # ID = 
        # print( )
        Update = "Update Bemor set mfamilya='%s', mismi='%s', mobileno='%s', pasport='%s', dob='%s' where ID='%s'" % (
        Bemor_Familya, Bemor_Ismi, Phone_Number, pasport,DOB, ID)
        db_cursor.execute(Update)
        db_connection.commit()
        mb.showinfo("Info", "O'zgartirildi")
        self.load_Bemor_data()

    def load_Bemor_data(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        self.calDOB.delete(0, tk.END)
        self.tvBemor.delete(*self.tvBemor.get_children()) 
        db_cursor.execute("use Bemor") 
        sql = "SELECT ID,mfamilya,mismi,pasport,mobileno,date_format(dob,'%d-%m-%Y') FROM Bemor"
        db_cursor.execute(sql)
        total = db_cursor.rowcount
        #if total ==0:
            #mb.showinfo("Info", "Nothing To Display,Please add data")
            #return
        print("Total Data Entries:" + str(total))
        rows = db_cursor.fetchall()

        ID = ""
        Bemor_Familya = ""
        Bemor_Ismi = ""
        pasport = ""
        Phone_Number = ""
        DOB =""
        for row in rows:
            ID = row[0]
            Bemor_Familya = row[1]
            Bemor_Ismi = row[2]
            pasport = row[3]
            Phone_Number = row[4]
            DOB = row[5]
            ddd =  datetime.strptime(DOB, "%d-%m-%Y").date()
            DOB = ddd.strftime('%Y-%m-%d')

            self.tvBemor.insert("", 'end', text=ID, values=(ID, Bemor_Familya, Bemor_Ismi, pasport, Phone_Number,DOB))




if __name__ == "__main__":
    app = BemorApp()
    app.mainloop()