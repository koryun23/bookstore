from tkinter import *
from backend import Database

database = Database()

class Window:
    def __init__(self, window):
        self.window = window

        self.window.wm_title("Book Store")
        #Labels
        title_label = Label(window, text="Title")
        title_label.grid(row=0,column=0)
        author_label = Label(window, text = "Author")
        author_label.grid(row=0, column=2)
        year_label = Label(window, text="Year")
        year_label.grid(row=1,column=0)
        isbn_label = Label(window, text="ISBN")
        isbn_label.grid(row=1,column=2)
        #Entry widgets
        self.title_text = StringVar() 
        self.title_entry = Entry(window, textvariable=self.title_text)
        self.title_entry.grid(row=0, column=1)

        self.author_text = StringVar()
        self.author_entry = Entry(window, textvariable=self.author_text)
        self.author_entry.grid(row=0, column = 3)

        self.year_text = StringVar()
        self.year_entry= Entry(window,  textvariable=self.year_text)
        self.year_entry.grid(row=1, column=1)

        self.isbn_text = StringVar()
        self.isbn_entry= Entry(window,  textvariable=self.isbn_text)
        self.isbn_entry.grid(row=1, column=3)

        #Buttons
        view_btn = Button(window, text="View All", width=15, height=1, command=self.view_command)
        view_btn.grid(row=2, column=3)
        search_btn = Button(window, text="Search entry",width=15, height=1, command=self.search_command)
        search_btn.grid(row=3, column=3)
        add_btn = Button(window, text="Add entry",width=15, height=1, command=self.add_command)
        add_btn.grid(row=4, column=3)
        update_btn = Button(window, text = "Update", width=15, height=1, command=self.update_command)
        update_btn.grid(row=5, column=3)
        delete_btn = Button(window, text="Delete",width=15, height=1, command=self.delete_command)
        delete_btn.grid(row=6, column=3)
        close_btn = Button(window, text="Close", width=15, height=1, command=self.window.destroy)
        close_btn.grid(row=7, column=3)
        #Listbox
        self.listbox = Listbox(window, height=12, width=35)

        self.listbox.grid(row=2, column=0, rowspan=6,columnspan=2)
        #scrollbar
        sb = Scrollbar(window)
        sb.grid(row=2, column=2, rowspan=6)

        self.listbox.configure(yscrollcommand=sb.set)
        sb.configure(command=self.listbox.yview)

        self.listbox.bind('<<ListboxSelect>>',self.get_selected_row)

    def get_selected_row(self,event):
        global selected_tuple
        if self.listbox.size() > 0 and self.listbox.curselection():
            index = self.listbox.curselection()[0]
            selected_tuple = self.listbox.get(index)
            self.title_entry.delete(0, END)
            self.title_entry.insert(END, selected_tuple[1])
            self.author_entry.delete(0, END)
            self.author_entry.insert(END, selected_tuple[2])
            self.year_entry.delete(0, END)                 
            self.year_entry.insert(END, selected_tuple[3])
            self.isbn_entry.delete(0,END)
            self.isbn_entry.insert(END, selected_tuple[4])

    def view_command(self):
        self.listbox.delete(0, END)
        for row in database.view():
            self.listbox.insert(END, row)
    def search_command(self):
        self.listbox.delete(0,END)
        for row in database.search(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()):
            self.listbox.insert(END, row)
    def add_command(self):
        database.insert(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.view_command()
        self.title_entry.delete(0,END)
        self.year_entry.delete(0,END)
        self.author_entry.delete(0,END)
        self.isbn_entry.delete(0,END)

    def delete_command(self):
        database.delete(selected_tuple[0])
        self.view_command()

    def update_command(self):
        database.update(selected_tuple[0],self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.view_command()

window = Tk()
Window(window)
window.mainloop()