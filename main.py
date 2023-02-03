import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk


#Connection Later

def connection():
    conn=pymysql.connect(
        host='localhost', user='root', password='', db='student_db'
    )
    return conn

def refreshtable():
    for data in my_tree.get_children():
        my_tree.delete(data)
    for array in read():
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

    my_tree.tag_configure('orwo', background='#EEEEEE', font=('Arial', 12))
    my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)


#GUI

root=Tk()
root.title("Student Registration System")
root.geometry("1080x720")
my_tree = ttk.Treeview(root)

#Function Later

#Place holder for entry

ph1=tk.StringVar()
ph2=tk.StringVar()
ph3=tk.StringVar()
ph4=tk.StringVar()
ph5=tk.StringVar()

#Set Place holder value

def setph(word, num):
    if num==1:
        ph1.set(word)
    if num==2:
        ph2.set(word)
    if num==3:
        ph3.set(word)
    if num==4:
        ph4.set(word)
    if num==5:
        ph5.set(word)


def read():
    conn = connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM students")
    results=cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def add():
    studid=str(studidEntry.get())
    fname = str(fnameEntry.get())
    lname = str(lnameEntry.get())
    address = str(addressEntry.get())
    phone = str(phoneEntry.get())

    if (studid=='' or studid==" ") or (fname=="" or fname==" ") or (lname=="" or lname==" ") or (address=="" or address==" ") or (phone=="" or phone==" "):
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students VALUES ('"+studid+"', '"+fname+"', '"+lname+"', '"+address+"', '"+phone+"')")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Student ID already exist!")
            return

    refreshtable()


def reset():
    decision=messagebox.askquestion("Warning!", "Dalete All Data?")
    if decision != "yes":
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an Error occured!")
            return
    refreshtable()


def delete():
    decision = messagebox.askquestion("Warning!", "Dalete all selected data?")
    if decision != "yes":
        return
    else:
        selected_item=my_tree.selection()[0]
        deleteData=str(my_tree.item(selected_item)['values'][0])
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE STUDID='"+str(deleteData)+"'")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an Error occured!")
            return
    refreshtable()


def select():
    try:
        selected_item=my_tree.selection()[0]
        studid=str(my_tree.item(selected_item)['values'][0])
        fname = str(my_tree.item(selected_item)['values'][1])
        lname = str(my_tree.item(selected_item)['values'][2])
        address = str(my_tree.item(selected_item)['values'][3])
        phone = str(my_tree.item(selected_item)['values'][4])

        setph(studid, 1)
        setph(fname, 2)
        setph(lname, 3)
        setph(address, 4)
        setph(phone, 5)
    except:
        messagebox.showinfo("Error", "Please select a data row")



def search():
    studid=str(studidEntry.get())
    fname = str(studidEntry.get())
    lname = str(studidEntry.get())
    address = str(studidEntry.get())
    phone = str(studidEntry.get())

    conn=connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM students WHERE STUDID='"+
    studid+"' or FNAME='"+
    fname+"' or  LNAME='"+
    lname+"' or ADDRESS='"+
    address+"' or PHONE='"+
    phone+"' ")


    try:
        result=cursor.fetchall()
        for num in range(0,5):
            setph(result[0][num], (num+1))
        conn.commit()
        conn.close()
    except:
        messagebox.showinfo("Error", "No data found!")


def update():
    selectedStudid=""
    try:
        selected_item=my_tree.selection()[0]
        selectedStudid=str(my_tree.item(selected_item)['values'][0])
    except:
        messagebox.showinfo("Error", "Please select a data row")

    studid = str(studidEntry.get())
    fname = str(studidEntry.get())
    lname = str(studidEntry.get())
    address = str(studidEntry.get())
    phone = str(studidEntry.get())

    if (studid == '' or studid == " ") or (fname == "" or fname == " ") or (lname == "" or lname == " ") or (address == "" or address == " ") or (phone == "" or phone == " "):
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE students SET STUDID='" +
            studid + "' , FNAME='" +
            fname + "'  , LNAME='" +
            lname + "' , ADDRESS='" +
            address + "' , PHONE='" +
            phone + "'WHERE STUDID='"+
            selectedStudid+"' ")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Student ID already exist!")
            return

    refreshtable()

#GUI


label=Label(root, text="Student Registration System (CRUD)", font=("Arial Bold", 30))
label.grid(row=0, column=0, columnspan=8, rowspan=2, padx=50, pady=40)

studidLabel=Label(root, text="Student ID", font=("Arial", 15))
fnameLabel=Label(root, text="First Name", font=("Arial", 15))
lnameLabel=Label(root, text="Last Name", font=("Arial", 15))
addressLabel=Label(root, text="Address", font=("Arial", 15))
phoneLabel=Label(root, text="Phone #", font=("Arial", 15))

studidLabel.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
fnameLabel.grid(row=4, column=0, columnspan=1, padx=50, pady=5)
lnameLabel.grid(row=5, column=0, columnspan=1, padx=50, pady=5)
addressLabel.grid(row=6, column=0, columnspan=1, padx=50, pady=5)
phoneLabel.grid(row=7, column=0, columnspan=1, padx=50, pady=5)


#Text Variable

studidEntry=Entry(root, width=55, bd=5, font=("Arial", 15), textvariable=ph1)
fnameEntry=Entry(root, width=55, bd=5, font=("Arial", 15), textvariable=ph2)
lnameEntry=Entry(root, width=55, bd=5, font=("Arial", 15), textvariable=ph3)
addressEntry=Entry(root, width=55, bd=5, font=("Arial", 15), textvariable=ph4)
phoneEntry=Entry(root, width=55, bd=5, font=("Arial", 15), textvariable=ph5)


studidEntry.grid(row=3, column=1, columnspan=4, padx=5, pady=0)
fnameEntry.grid(row=4, column=1, columnspan=4, padx=5, pady=0)
lnameEntry.grid(row=5, column=1, columnspan=4, padx=5, pady=0)
addressEntry.grid(row=6, column=1, columnspan=4, padx=5, pady=0)
phoneEntry.grid(row=7, column=1, columnspan=4, padx=5, pady=0)


#Command Later

addBtn = Button(
    root,text="Add",padx=65, pady=25, width=10, bd=5, font=("Arial", 15), bg="#84F894", command=add
)

updateBtn = Button(
    root,text="Update",padx=65, pady=25, width=10, bd=5, font=("Arial", 15), bg="#84E8F8", command=update
)

deleteBtn = Button(
    root,text="Delete",padx=65, pady=25, width=10, bd=5, font=("Arial", 15), bg="#FF9999", command=delete
)

searchBtn = Button(
    root,text="Search",padx=65, pady=25, width=10, bd=5, font=("Arial", 15), bg="#F4FE82", command=search
)

resetBtn = Button(
    root,text="Reset",padx=65, pady=25, width=10, bd=5, font=("Arial", 15), bg="#F389FF", command=reset
)

selectBtn = Button(
    root,text="Select",padx=65, pady=25, width=10, bd=5, font=("Arial", 15), bg="#EEEEEE", command=select
)

addBtn.grid(row=3, column=5, columnspan=1, rowspan=2)
updateBtn.grid(row=5, column=5, columnspan=1, rowspan=2)
deleteBtn.grid(row=7, column=5, columnspan=1, rowspan=2)
searchBtn.grid(row=9, column=5, columnspan=1, rowspan=2)
resetBtn.grid(row=11, column=5, columnspan=1, rowspan=2)
selectBtn.grid(row=13, column=5, columnspan=1, rowspan=2)

style=ttk.Style()
style.configure("Treeview.Heading", font=("Arial Bold",15))
my_tree['columns']= ("student ID", "First Name","Last Name", "Address", "Phone")


my_tree.column("#0", width=0, stretch=NO)
my_tree.column("student ID", anchor=W, width=170)
my_tree.column("First Name", anchor=W, width=150)
my_tree.column("Last Name", anchor=W, width=150)
my_tree.column("Address", anchor=W, width=165)
my_tree.column("Phone", anchor=W, width=150)

my_tree.heading("student ID", text="Student ID", anchor=W)
my_tree.heading("First Name", text="First Name", anchor=W)
my_tree.heading("Last Name", text="Last Name", anchor=W)
my_tree.heading("Address", text="Address", anchor=W)
my_tree.heading("Phone", text="Phone", anchor=W)


refreshtable()

root.mainloop()

