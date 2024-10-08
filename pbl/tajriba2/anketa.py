from tkinter import ttk
import tkinter as tk
import mysql.connector

import sys
id = 0
if("--id" in  sys.argv):
    id = sys.argv[sys.argv.index("--id") + 1]

# def create_table(self):
#         if db_connection.is_connected() == False:
#           db_connection.connect()
#         db_cursor.execute("CREATE DATABASE IF NOT EXISTS Bemor")  
#         db_cursor.execute("use Bemor")  
#         db_cursor.execute("create table if not exists anketa(Id INT(10) NOT NULL  PRIMARY KEY AUTO_INCREMENT,kelgan_sana datetime, tolov VARCHAR(30),eslatma text)AUTO_INCREMENT=1")
#         db_connection.commit()


def bemorshowinfo():
    global id
    con1 = mysql.connector.connect(host="localhost",
    user="root",
    password="",
    database='Bemor')   #BAZZQ OZGARTIRISH
    cur1 = con1.cursor()
    cur1.execute("SELECT * FROM Bemor where Id=" + str(id))
    rows = cur1.fetchall()    
    con1.close() 
    print(rows)
    return rows[0][1] + " " +  rows[0][2]






def anketashowinfo():
    global id
    con1 = mysql.connector.connect(host="localhost",
    user="root",
    password="",
    database='Bemor')   #BAZZQ OZGARTIRISH
    cur1 = con1.cursor()
    cur1.execute("SELECT * FROM anketa where id_bemor = " + str(id))
    rows = cur1.fetchall()
    print(rows)    
    con1.close() 
    

root = tk.Tk()
tree = ttk.Treeview(root, column=("c1", "c2"), show='headings')
tree.column("#1", anchor=tk.CENTER)
tree.heading("#1", text="Ismi")
tree.column("#2", anchor=tk.CENTER)
tree.heading("#2", text="Kelgan sana")

bemor_info = tk.Label(root).pack(pady=10)
tree.pack()
button1 = tk.Button(root, text="Bemorlar ro'yhadini ko'rish", command=anketashowinfo)
button1.pack(pady=10)

narxi = tk.Entry(root).pack(pady=10)
eslatma = tk.Entry(root).pack(pady=10)





def show_selected_record(tree, event):
        tree.clear_form()
        for selection in tree.tvBemor.selection():
            item = tree.tvBemor.item(selection)
        global id_ank
        id_bemor,kelgan_sana,tolov,eslatma,id = item["values"][0:7]
        tree.entkelgan_sana.insert(0, kelgan_sana)
        tree.enttolov .insert(0, tolov)
        tree.enteslatma.insert(0, eslatma)
        tree.calid.insert(0, id)
        return id

# # connect to the database

# root = tk.Tk()
# tree = ttk.Treeview(root, column=("c1", "c2"), show='headings')
# tree.column("#1", anchor=tk.CENTER)
# tree.heading("#1", text="Ismi")
# tree.column("#2", anchor=tk.CENTER)
# tree.heading("#2", text="Kelgan sana")

# bemor_info = tk.Label(root).pack(pady=10)
# tree.pack()
# button1 = tk.Button(root, text="Bemorlar ro'yhadini ko'rish", command=anketashowinfo)
# button1.pack(pady=10)

# narxi = tk.Entry(root).pack(pady=10)
# eslatma = tk.Entry(root).pack(pady=10)

# bemor_info.config(text=bemorshowinfo())

print(bemorshowinfo())
root.mainloop()