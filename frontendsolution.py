import sys
from tkinter import *
from tkinter import Toplevel
from tkinter import messagebox
from backend import Database

database=Database("books.db")



class Window(object):

    def __init__(self,window):

        self.window = window

        self.window.wm_title("BookStore")

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_menu()

        l1=Label(window,relief=RIDGE,text="Title")
        l1.grid(row=0,column=0)

        l2=Label(window,relief=RIDGE,text="Author")
        l2.grid(row=0,column=2)

        l3=Label(window,relief=RIDGE,text="Year")
        l3.grid(row=1,column=0)

        l4=Label(window,relief=RIDGE,text="Price")
        l4.grid(row=1,column=2)

        self.title_text=StringVar()
        self.e1=Entry(window,textvariable=self.title_text)
        self.e1.grid(row=0,column=1)

        self.author_text=StringVar()
        self.e2=Entry(window,textvariable=self.author_text)
        self.e2.grid(row=0,column=3)

        self.year_text=StringVar()
        self.e3=Entry(window,textvariable=self.year_text)
        self.e3.grid(row=1,column=1)

        self.price_text=StringVar()
        self.e4=Entry(window,textvariable=self.price_text)
        self.e4.grid(row=1,column=3)

        self.list1=Listbox(window, height=6,width=35)
        self.list1.grid(row=2,column=0,rowspan=6,columnspan=2,sticky=E+W+N+S)

        sb1=Scrollbar(window)
        sb1.grid(row=2,column=2,rowspan=6)

        self.list1.configure(yscrollcommand=sb1.set)
        sb1.configure(command=self.list1.yview)

        self.list1.bind('<<ListboxSelect>>',self.get_selected_row)

        b1=Button(window,text="View all", width=12,command=self.view_command)
        b1.grid(row=2,column=3)
        b1.config(bg="lightblue")

        b2=Button(window,text="Search entry", width=12,command=self.search_command)
        b2.grid(row=3,column=3)
        b2.config(bg="lightblue")

        b3=Button(window,text="Add entry", width=12,command=self.add_command)
        b3.grid(row=4,column=3)
        b3.config(bg="lightblue")

        b4=Button(window,text="Update selected", width=12,command=self.update_command)
        b4.grid(row=5,column=3)
        b4.config(bg="lightblue")

        b5=Button(window,text="Delete selected", fg="red", width=12,command=self.delete_command)
        b5.grid(row=6,column=3)
        b5.config(bg="lightblue")

        b6=Button(window,text="Close", width=12,command=root_window.destroy)
        b6.grid(row=7,column=3)
        b6.config(bg="lightblue")


    #Creation of init_window
    def init_menu(self):
        # creating a menu instance
        menu = Menu(self.window)
        self.window.config(menu=menu)


        file = Menu(menu)
        file.add_command(label="Customize", command=self.create_window)
        file.add_command(label="Exit", command=root_window.destroy)
        menu.add_cascade(label="File", menu=file)


        edit = Menu(menu)
        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)

    def get_selected_row(self,event):
        try:
            index=self.list1.curselection()[0]
        except IndexError:
            messagebox.showinfo("Error!", "Nothing available for select.")
            return
        self.selected_tuple=self.list1.get(index)
        self.e1.delete(0,END)
        self.e1.insert(END,self.selected_tuple[1])
        self.e2.delete(0,END)
        self.e2.insert(END,self.selected_tuple[2])
        self.e3.delete(0,END)
        self.e3.insert(END,self.selected_tuple[3])
        self.e4.delete(0,END)
        self.e4.insert(END,self.selected_tuple[4])

    def create_window(self):
        windows = Toplevel(root_window,bg="red",takefocus=True)
        windows.wm_title("Customize")

    def view_command(self):
        self.list1.delete(0,END)
        for row in database.view():
            self.list1.insert(END,row)

    def search_command(self):
        self.list1.delete(0,END)
        for row in database.search(self.title_text.get(),self.author_text.get(),self.year_text.get(),self.price_text.get()):
            self.list1.insert(END,row)

    def add_command(self):
        if self.title_text.get() == "" or self.author_text.get() == "" or self.year_text.get() == "" or self.price_text.get() == "" :
            messagebox.showinfo("Error!", "All fields are mandatory!")
            return
        try:
            val = float(self.price_text.get())
            if  "." not in self.price_text.get():
                messagebox.showinfo("Error!","Price must contain exactly 2 decimals!" )
            elif len(self.price_text.get().rsplit('.')[-1]) == 2 :
                database.insert(self.title_text.get(),self.author_text.get(),self.year_text.get(),self.price_text.get())
                self.list1.delete(0,END)
                self.list1.insert(END,(self.title_text.get(),self.author_text.get(),self.year_text.get(),self.price_text.get()))
            else:
                messagebox.showinfo("Error!","Price must contain exactly 2 decimals!" )
        except ValueError:
            messagebox.showinfo("Error!","Price must be a number!" )


    def delete_command(self):
        database.delete(self.selected_tuple[0])

    def update_command(self):
        if self.title_text.get() == "" or self.author_text.get() == "" or self.year_text.get() == "" or self.price_text.get() == "" :
            messagebox.showinfo("Error!", "All fields are mandatory!")
            return
        try:
            val = float(self.price_text.get())
            if  "." not in self.price_text.get():
                messagebox.showinfo("Error!","Price must contain exactly 2 decimals!" )
            elif len(self.price_text.get().rsplit('.')[-1]) == 2 :
                database.update(self.selected_tuple[0],self.title_text.get(),self.author_text.get(),self.year_text.get(),self.price_text.get())
                self.list1.delete(0,END)
                self.list1.insert(END,(self.title_text.get(),self.author_text.get(),self.year_text.get(),self.price_text.get()))
            else:
                messagebox.showinfo("Error!","Price must contain exactly 2 decimals!" )
        except ValueError:
            messagebox.showinfo("Error!","Price must be a number!" )



root_window=Tk()

#prepair all the necessary things (data) to center window on screen
# Gets the requested values of the height and widht.
windowWidth = root_window.winfo_reqwidth()
windowHeight = root_window.winfo_reqheight()
print("Width",windowWidth,"Height",windowHeight)

# Gets both half the screen width/height and window width/height
positionRight = int(root_window.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root_window.winfo_screenheight()/2 - windowHeight/2)

# Positions the window in the center of the page.
root_window.geometry("+{}+{}".format(positionRight, positionDown))
root_window.resizable(False, False)
Window(root_window)
root_window.mainloop()
