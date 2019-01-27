from Tkinter import *
import tkMessageBox
import pandas as pd
import sqlite3
from datetime import datetime
import time

################################################################################

d = datetime.now()
datet = d.date()
datet = str(datet)
datet = datet.split("-")
date = datet[2]
month = datet[1]
day = datetime.today().weekday()
montharr = [month]
weekarr = [day]

################################################################################

class Project:
    def __init__(self):
        self.data = sqlite3.connect(":memory:")
        self.data1 = self.data.cursor()
        try:
            self.db = self.data1.execute("CREATE TABLE primtable(card integer primary key NOT NULL, name NOT NULL, clothes integer NOT NULL)")
            self.data2 = self.data1.execute("CREATE TABLE monthtable(card integer primary key NOT NULL, name NOT NULL, clothes integer NOT NULL)")
        except sqlite3.OperationalError:
            pass
        if weekarr[0] != day:
            self.db.execute("delete from primtable")
            self.db.execute("VACUUM")
            weekarr[0] = day
        if montharr[0] != month:
            self.data2.execute("delete from monthtable")
            self.data2.execute("VACUUM")
            montharr[0] = month
        self.top = Tk()

        self.mainmenu = Menu(self.top)

        self.filemenu = Menu(self.mainmenu)
        self.filemenu.add_command(label="New", command=self.new)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.top.quit)
        self.mainmenu.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = Menu(self.mainmenu)
        self.editmenu.add_command(label="Customer List",command = self.printer)
        self.editmenu.add_command(label="Update",command = self.printer)
        self.editmenu.add_command(label="Undo",command = self.printer)
        self.editmenu.add_command(label="Delete",command = self.delete)
        self.mainmenu.add_cascade(label="Edit", menu=self.editmenu)

        self.toolmenu = Menu(self.mainmenu)
        self.toolmenu.add_command(label="Weeks's List",command = self.weeks_list)
        self.toolmenu.add_command(label="Month's list",command = self.months_list)
        self.toolmenu.add_command(label="Fees",command = self.printer)
        self.mainmenu.add_cascade(label="View", menu=self.toolmenu)

        self.top.config(menu=self.mainmenu)

        self.leftframe = Frame(self.top,height = 1000,width = 1000,relief = RAISED,bd = 4,highlightcolor = "Yellow",highlightbackground = "Black")
        self.leftframe.pack(fill = BOTH,expand = TRUE,side = LEFT)

        self.mainlabel1 = Label(self.leftframe,text = "Check-IN",bg = "blue",fg = "white",font = "Verdana 15 bold",padx = 80,pady = 20,relief = RAISED)
        self.mainlabel1.pack(fill = X)

        self.minileftframe = Frame(self.leftframe)
        self.minileftframe.pack(fill=Y, side=TOP)

        self.namelabel = Label(self.minileftframe, text="Name",relief = RAISED,padx = 54)
        self.cardlabel = Label(self.minileftframe, text="Card",relief = RAISED, padx = 57)
        self.clotheslabel = Label(self.minileftframe, text="Clothes",relief = RAISED, padx = 50)
        self.namelabel.grid(row=2, column=1,)
        self.cardlabel.grid(row=4, column=1,)
        self.clotheslabel.grid(row=6, column=1,)

        self.namevar = StringVar()
        self.name = Entry(self.minileftframe,textvariable = self.namevar)
        self.clothesvar = StringVar()
        self.clothes = Entry(self.minileftframe,textvariable = self.clothesvar)
        self.cardvar = StringVar()
        self.card = Entry(self.minileftframe,textvariable = self.cardvar)
        self.name.grid(row = 2,column = 2)
        self.clothes.grid(row = 4, column = 2)
        self.card.grid(row = 6, column = 2)

        self.entrybutton = Button(self.minileftframe, text="Enter",command = self.get_info,padx = 30,bg = "blue",fg = "white",font = "Verdana 12 bold",relief = RAISED)
        self.entrybutton.grid(row=8, column=1, columnspan=2)

        self.rightframe = Frame(self.top,height = 200,width = 100,bd = 4,relief = RAISED)
        self.rightframe.pack(fill = BOTH,expand = TRUE,side = RIGHT)

        self.mainlabel2 = Label(self.rightframe, text="Check-OUT",font = "Verdana 15 bold", bg="Red", fg="white", pady=20, relief=RAISED)
        self.mainlabel2.pack(fill = X, side = TOP)

        self.minirightframe = Frame(self.rightframe)
        self.minirightframe.pack(fill = Y,side = TOP)

        self.exitlabel = Label(self.minirightframe, text="CardNumber",relief = RAISED,padx = 25)
        self.exitlabel.grid(row=4, column=10)
        self.exitvar = StringVar()
        self.exit = Entry(self.minirightframe, textvariable=self.exitvar)
        self.exit.grid(row=4, column=11,columnspan  = 2)

        self.exitbutton = Button(self.minirightframe, text="Check-Out",command = self.remove_info,padx = 20,bg = "red",fg = "white",font = "Verdsna 12 bold",relief = RAISED)
        self.exitbutton.grid(row=6, column=10, columnspan=3)

        self.savebutton = Button(self.top,text = "Save",command = self.printer,bg = "Black",fg = "White",relief = RAISED)
        self.savebutton.pack(fill =Y,expand = TRUE,side = BOTTOM)

        self.top.mainloop()

    def add_week_info(self,card,name,clothes):
        card = int(card)
        clothes = int(clothes)
        if clothes <= 15:
            try:
                self.db = self.db.execute("insert into primtable(card,name,clothes) values (?,?,?)",(card,name,clothes))
            except sqlite3.IntegrityError:
                pass
            finally:
                self.db = self.db
                self.add_months_list(card, name, clothes)
                return self.db
        else:
            tkMessageBox.showerror("Status","Cannot add more than 15 clothes")
    def add_months_list(self,card,name,clothes):
        try:
            self.data2 = self.data2.execute("insert into monthtable(card,name,clothes) values (?,?,?)", (card,name,clothes))
            tkMessageBox.showinfo("Status", "Done Adding")
        except sqlite3.IntegrityError:
            temp = self.data.cursor()
            temp = temp.execute("select clothes from monthtable where card = ?",(card,))
            temp = temp.fetchall()
            for i in temp:
                for j in i:
                    var1 = j
            var1 = int(var1) +int(clothes)
            if var1 <= 60:
                self.data2 = self.data2.execute("update monthtable set clothes = ? where card = ?",(var1,card))
                tkMessageBox.showinfo("Status", "Done Adding")
            else:
                tkMessageBox.showerror("Status",["You can only give",60-var1,"\nClothes for the month"])
        finally:
            return self.data2
    def get_info(self):
        try:
            l1 = [self.cardvar.get(),self.namevar.get(),int(self.clothesvar.get())]
        except ValueError:
            tkMessageBox.showerror("Status","Enter correct information")
        else:
            try:
                var = self.add_week_info(l1[2],l1[1],l1[0])
            except ValueError:
                tkMessageBox.showerror("Status", "Enter correct information")
        finally:
            self.name.delete(0, END)
            self.card.delete(0, END)
            self.clothes.delete(0, END)
            try:
                return var
            except UnboundLocalError:
                pass
    def weeks_list(self):
        self.db1 = self.db.execute("select * from primtable order by card ASC")
        dbb = list(self.db1)
        dbb = pd.DataFrame(dbb,columns = ["Card","Name","Clothes"])
        self.newindow(dbb)
    def months_list(self):
        self.var = self.data2.execute("select * from monthtable order by card ASC")
        dbb = list(self.var)
        dbb = pd.DataFrame(dbb,columns = ["Card","Name","Clothes"])
        self.newindow(dbb)
    def newindow(self,text):
        window = Tk()
        label = Label(window,text = text)
        label.grid(row = 1,columnspan = 10)
        button = Button(window,text = "OK",command = window.withdraw)
        button.grid(row = 3,column = 5)
        window.mainloop()
    def del_info(self,card):
        self.db = self.db.execute("delete from primtable where card = ?",[card])
        return self.db
    def remove_info(self):
        var = self.del_info(self.exitvar.get())
        tkMessageBox.showinfo("Status","Done Deleting")
        self.exit.delete(0,END)
        return var
    def delete(self):
        radiovar = IntVar()
        def delfunction():
            if radiovar.get() == 1:
                self.db = self.db.execute("delete from primtable where card = ?", (self.exitvar.get(),))
                tkMessageBox.showinfo("Status", "Done Deleting1")
                self.exit.delete(0, END)
            elif radiovar.get() == 2:
                self.data2 = self.data2.execute("delete from monthtable where card = ?", (self.exitvar.get(),))
                tkMessageBox.showinfo("Status", "Done Deleting2")
                self.exit.delete(0, END)
            else:
                tkMessageBox.showerror("Status", "Select valid option")
                self.exit.delete(0, END)
        Radiobutton(self.minirightframe, text="Week's List", variable=radiovar,value = 1,indicatoron = 0,padx = 29,command = delfunction).grid(row=5,column= 10)
        Radiobutton(self.minirightframe, text="Month's List", variable=radiovar,value = 2,indicatoron = 0,padx = 26,command = delfunction).grid(row=5, column =11)
    def new(self):
        self.db.execute("delete from primtable")
        self.db.execute("VACUUM")
        self.data2.execute("delete from monthtable")
        self.data2.execute("VACUUM")
        tkMessageBox.showinfo("Status","New table created")
    def printer(self):
        tkMessageBox.showinfo("Status","This function has\nnot been updated")







obj = Project()
time.sleep(5)