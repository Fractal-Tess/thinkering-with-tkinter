from tkinter import *
import sqlite3
from tkinter import messagebox

Root = Tk()
Root.title("Database")

Connect = sqlite3.connect('My_Dates.db')
c = Connect.cursor()

'''c.execute("""CREATE TABLE birthdays (
    Email text,
    Username text,
    Password text,
    Year integer
    )""")'''

def NewEntry():
    try:
        Connect = sqlite3.connect('My_dates.db')
        c = Connect.cursor()
        if E_Name.get() == "":
            error_handler = int(E_Name.get())
        c.execute("INSERT INTO birthdays VALUES (:Name, :Date, :Month, :Year)",
                  {
                'Name': str(E_Name.get()),
                'Date': str(int(E_Date.get())),
                'Month': str(int(E_Month.get())),
                'Year': str(int(E_Year.get()))

                  })
        E_Name.delete(0, END)
        E_Date.delete(0, END)
        E_Month.delete(0, END)
        E_Year.delete(0, END)

        Connect.commit()
        Connect.close()

        Query()
    except:
        try:
            Connect = sqlite3.connect('My_dates.db')
            c = Connect.cursor()

            c.execute("""CREATE TABLE birthdays (
                Name text,
                Date integer,
                Month integer,
                Year integer
                )""")

            Connect.commit()
            Connect.close()
        except:
            Error = messagebox.showerror("Error!", "Error occured, possible reasons:\n--Name/Date/Month/Year are invalid!\n--Failed to connect!")
    return

def Query():
    Connect = sqlite3.connect('My_dates.db')
    c = Connect.cursor()

    c.execute("SELECT *, oid FROM birthdays")
    Records = c.fetchall()

    Print_Rec = ""
    for record in Records:
        Print_Rec += str(record[4]) + ") " + str(record[0]) + ": " + str(record[1]) + "." + str(record[2]) + "." + str(record[3]) + "\n"

    L_ShowRec = Label(Root, text=Print_Rec)
    L_ShowRec.grid(row=9, column=0, columnspan=2)

    Connect.commit()
    Connect.close()
    return

def Delete():
    Confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete ID " + str(E_Select.get()) + " ?")
    if Confirm == 1:
        Connect = sqlite3.connect('My_dates.db')
        c = Connect.cursor()

        c.execute("DELETE from birthdays WHERE oid = " + str(E_Select.get()))
        E_Select.delete(0, END)

        Connect.commit()
        Connect.close()

        Query()
    return

def Update():
    try:
        Connect = sqlite3.connect('My_dates.db')
        c = Connect.cursor()

        c.execute("""UPDATE birthdays SET
                Name = :Name,
                Date = :Date,
                Month = :Month,
                Year = :Year
                WHERE oid = :oid""",
                {
                'Name':str(E_NameEdit.get()),
                'Date':str(int(E_DateEdit.get())),
                'Month':str(int(E_MonthEdit.get())),
                'Year':str(int(E_YearEdit.get())),
                'oid':str(Edit_Id)

                })

        Connect.commit()
        Connect.close()

        Query()
    except:
        Error = messagebox.showerror("Error!","Error occured, possible reasons:\n--Name/Date/Month/Year are invalid!\n--Failed to connect!")
    Editor.destroy()
    return

def Edit():
    try:
        global Editor
        Editor = Tk()
        Editor.title("Update Record")

        global E_NameEdit
        global E_DateEdit
        global E_MonthEdit
        global E_YearEdit

        E_NameEdit = Entry(Editor)
        E_DateEdit = Entry(Editor)
        E_MonthEdit = Entry(Editor)
        E_YearEdit = Entry(Editor)

        L_Name = Label(Editor, text="Enter Name:")
        L_Date = Label(Editor, text="Enter birth day:")
        L_Month = Label(Editor, text="Enter birth month:")
        L_Year = Label(Editor, text="Enter birth Year:")

        B_Save = Button(Editor, text="Update Entry", width=33, command=Update)

        L_Name.grid(row=0, column=0)
        L_Date.grid(row=1, column=0)
        L_Month.grid(row=2, column=0)
        L_Year.grid(row=3, column=0)

        E_NameEdit.grid(row=0, column=1)
        E_DateEdit.grid(row=1, column=1)
        E_MonthEdit.grid(row=2, column=1)
        E_YearEdit.grid(row=3, column=1)

        B_Save.grid(row=4, column=0, columnspan=2)

        Connect = sqlite3.connect('My_dates.db')
        c = Connect.cursor()

        global Edit_Id
        Edit_Id = int(E_Select.get())
        c.execute("SELECT * FROM birthdays WHERE oid =" + str(Edit_Id))
        Records = c.fetchall()

        for record in Records:
            E_NameEdit.insert(0, record[0])
            E_DateEdit.insert(0, record[1])
            E_MonthEdit.insert(0, record[2])
            E_YearEdit.insert(0, record[3])

        Connect.commit()
        Connect.close()
        #Editor.destroy()
    except:
        Error = messagebox.showerror("Error!","Error occured, possible reasons:\n--Invalid ID!\n--Failed to connect!")
        Editor.destroy()
    return

# DECLARATIONS
E_Name = Entry(Root)
E_Date = Entry(Root)
E_Month = Entry(Root)
E_Year = Entry(Root)
E_Select = Entry(Root)

L_Name = Label(Root, text="Enter Name:")
L_Date = Label(Root, text="Enter birth day:")
L_Month = Label(Root, text="Enter birth month:")
L_Year = Label(Root, text="Enter birth Year:")
L_Select = Label(Root, text="Select entry # :")

B_Submit = Button(Root, text="Insert Entry", width=33, command=NewEntry)
B_Query = Button(Root, text="Show Entries", width=33, command=Query)
B_Delete = Button(Root, text="Delete Entry", width=33, command=Delete)
B_Edit = Button(Root, text="Edit Entry", width=33, command=Edit)

# GRIDING
L_Name.grid(row=0, column=0)
L_Date.grid(row=1, column=0)
L_Month.grid(row=2, column=0)
L_Year.grid(row=3, column=0)
L_Select.grid(row=6, column=0)

E_Name.grid(row=0, column=1)
E_Date.grid(row=1, column=1)
E_Month.grid(row=2, column=1)
E_Year.grid(row=3, column=1)
E_Select.grid(row=6, column=1)

B_Submit.grid(row=4, column=0, columnspan=2)
B_Query.grid(row=5, column=0, columnspan=2)
B_Delete.grid(row=7, column=0, columnspan=2)
B_Edit.grid(row=8, column=0, columnspan=2)


Connect.commit()
Connect.close()

Root.mainloop()