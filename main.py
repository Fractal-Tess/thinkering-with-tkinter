try:
    from tkinter import *
    import sqlite3
    from tkinter import messagebox
    from os import path
except Exception as e:
    print("You are missing some modules!: " + e)

Root = Tk()
Root.title("Account Manager")

if not path.exists("accounts.db"):
    connect = sqlite3.connect("accounts.db")
    c = connect.cursor()
    with connect:
        c.execute("""CREATE TABLE Accounts(
             Title text,
             Email text,
             Username text,
             Password text,
             Description text
             )""")
    print("Making new .db")


# connect  = sqlite3.connect(':memory:") - for memory db


def NewEntry():
    connect = sqlite3.connect("accounts.db")
    c = connect.cursor()
    with connect:
        c.execute("INSERT INTO Accounts VALUES (:Title, :Email, :Username, :Password, :Description)",
                  {
                      'Title': str(E_Title.get()),
                      'Email': str(E_Email.get()),
                      'Username': str(E_Username.get()),
                      'Password': str(E_password.get()),
                      'Description': str(E_Description.get())
                  })
    E_Title.delete(0, END)
    E_Email.delete(0, END)
    E_Username.delete(0, END)
    E_password.delete(0, END)
    E_Description.delete(0, END)
    return


def Query():
    Connect = sqlite3.connect('Accounts.db')
    c = Connect.cursor()

    c.execute("SELECT *, oid FROM Accounts")
    Records = c.fetchall()

    Print_Rec = ""
    for record in Records:
        Print_Rec += str(record[4]) + ") " + str(record[0]) + ": " + str(record[1]) + "." + str(record[2]) + "." + str(
            record[3]) + "\n"

    L_ShowRec = Label(Root, text=Print_Rec)
    L_ShowRec.grid(row=9, column=0, columnspan=2)

    Connect.commit()
    Connect.close()
    return


def Delete():
    Confirm = messagebox.askyesno("Confirm Delete",
                                  "Are you sure you want to delete ID " + str(E_Description.get()) + " ?")
    if Confirm == 1:
        Connect = sqlite3.connect('My_dates.db')
        c = Connect.cursor()

        c.execute("DELETE from birthdays WHERE oid = " + str(E_Description.get()))

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
                      'Name': str(E_NameEdit.get()),
                      'Date': str(int(E_DateEdit.get())),
                      'Month': str(int(E_MonthEdit.get())),
                      'Year': str(int(E_YearEdit.get())),
                      'oid': str(Edit_Id)

                  })

        Connect.commit()
        Connect.close()

        Query()
    except:
        Error = messagebox.showerror("Error!",
                                     "Error occured, possible reasons:\n--Name/Date/Month/Year are invalid!\n--Failed to connect!")
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
        Edit_Id = int(E_Description.get())
        c.execute("SELECT * FROM birthdays WHERE oid =" + str(Edit_Id))
        Records = c.fetchall()

        for record in Records:
            E_NameEdit.insert(0, record[0])
            E_DateEdit.insert(0, record[1])
            E_MonthEdit.insert(0, record[2])
            E_YearEdit.insert(0, record[3])

        Connect.commit()
        Connect.close()
        # Editor.destroy()
    except:
        Error = messagebox.showerror("Error!", "Error occured, possible reasons:\n--Invalid ID!\n--Failed to connect!")
        Editor.destroy()
    return


# DECLARATIONS

E_Title = Entry(Root)
E_Email = Entry(Root)
E_Username = Entry(Root)
E_password = Entry(Root)
E_Description = Entry(Root)

L_Title = Label(Root, text="Title")
L_Email = Label(Root, text="Email")
L_Username = Label(Root, text="Username")
L_Password = Label(Root, text="Password")
L_Description = Label(Root, text="Description")

B_Save = Button(Root, text="Save", width=33, command=NewEntry)

B_Query = Button(Root, text="Show Entries", width=33, command=Query)
B_Delete = Button(Root, text="Delete Entry", width=33, command=Delete)
B_Edit = Button(Root, text="Edit Entry", width=33, command=Edit)

# GRIDING
L_Title.grid(row=0, column=0)
L_Email.grid(row=1, column=0)
L_Username.grid(row=2, column=0)
L_Password.grid(row=3, column=0)
L_Description.grid(row=4, column=0)

E_Title.grid(row=0, column=1)
E_Email.grid(row=1, column=1)
E_Username.grid(row=2, column=1)
E_password.grid(row=3, column=1)
E_Description.grid(row=4, column=1)

B_Save.grid(row=5, column=0, columnspan=2)

Root.mainloop()
