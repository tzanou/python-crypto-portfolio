# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import Separator
from backend import Database
from api import API





class Investment:
    def __init__(self,name,amount,bought_rate,currency):
        self.name=name
        self.amount = amount
        self.price_bought = bought_rate
        self.currency = currency

    def calculate(self):
        return self.amount* self.current_rate


class View:



    def __init__(self, master,rows):
        self.rows=rows
        self.frame = master
        self.currency_symbols = {"USD": "$", "EUR": "€"}
        self.top_frame=Frame(self.frame,height=30)
        self.middle_frame = Frame(self.frame)
        self.bottom_frame = Frame(self.frame)
        self.top_frame.pack()
        self.middle_frame.pack()
        self.bottom_frame.pack()

        self.coin_label=Label(self.top_frame,text="Coin",width=10,bg="grey")
        self.coin_label.pack(side=LEFT)

        self.coin_label = Label(self.top_frame, text="Value",width=10,bg="grey")
        self.coin_label.pack(side=LEFT)

        self.gain_label = Label(self.top_frame, text="Gain",width=10,bg="grey")
        self.gain_label.pack(side=LEFT)

        self.coin_label = Label(self.top_frame, text="Amount",width=10,bg="grey")
        self.coin_label.pack(side=LEFT)

        self.coin_label = Label(self.top_frame, text="Price",width=10,bg="grey")
        self.coin_label.pack(side=LEFT)
        self.canvas_row=2
        self.canvas_column = 0
        self.canvas_rowspan = 0
        self.canvas_columnspan = 8
        self.canvas = Canvas(self.middle_frame,width=400,height=(20*(rows-1)))
        self.canvas.pack(side=LEFT)

        self.scrollbar = Scrollbar(self.middle_frame, command=self.canvas.yview)
        if rows-1>10:
            self.scrollbar.pack(side=LEFT)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        self.canvas.bind('<Configure>', self.OnFrameConfigure)

        self.canvas_frame = Frame(self.canvas)
        self.canvas.create_window((250, 0), window=self.canvas_frame)




        self.add_button = Button(self.bottom_frame, text="Add")
        self.add_button.pack(side=LEFT)

        self.reload_button = Button(self.bottom_frame, text="Reload")
        self.reload_button.pack(side=LEFT)



    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def popup_is_displayed(self):
        if hasattr(self, 'win'):
            return self.win.winfo_exists()
        else:
            return FALSE

    def add_investment(self,dummy,db):
        all_symbols= db.get_coin_symbols()
        print("Symbol : ",self.symbol_var.get().lower() )

        self.l = Label(self.win, text="")
        if self.symbol_var.get()=="":
            self.l['text'] =("Empty Symbol")
        elif self.symbol_var.get().upper() not in all_symbols:
            self.l['text'] =("Symbol not recognized")
        elif not  self.is_number(self.amount_var.get()):
            self.l['text'] =("Amount is not a number")
        elif not  self.is_number(self.price_var.get()):
            self.l['text'] =("Price is not a number")
        else :
            inve=Investment(db.get_coin_name(self.symbol_var.get().upper()),float(self.amount_var.get()),float(self.price_var.get()),self.currency_var.get())
            db.insert_investment(inve)


        if self.l['text']!="":
            self.l.grid(row=4, column=1)
        else :
            #self.load_investments(db)
            self.win.destroy()

    def create_loading_popup(self,):
        


        if self.popup_is_displayed():
            return

        self.win = Toplevel(width=300, height=200)
        self.win.focus_set()

        self.win.grab_set()

        self.win.transient(self.frame)


        self.win.wm_title("Loading")

        self.loading_text = Label(self.win, text="Loading coins...Please wait")
        self.loading_text.pack()


        self.win.update()


    def create_popup(self,event):
        if self.popup_is_displayed():
            return

        self.win = Toplevel()

        self.win.focus_set()

        self.win.grab_set()

        self.win.transient(self.frame)
        self.win.wm_title("Add Investment")

        self.coin_label = Label(self.win, text="Coin Symbol")
        self.coin_label.grid(row=0, column=0)

        self.symbol_var = StringVar()
        self.symbol_input = Entry(self.win,textvariable=self.symbol_var)
        self.symbol_input.grid(row=0, column=1)

        self.amount_label = Label(self.win, text="Amount")
        self.amount_label.grid(row=1, column=0)

        self.amount_var = StringVar()
        self.amount_input = Entry(self.win,textvariable=self.amount_var)
        self.amount_input.grid(row=1, column=1)

        self.currency_label = Label(self.win, text="Currency")
        self.currency_label.grid(row=2, column=0)

        self.currency_var = StringVar(self.win)
        self.currency_var.set("USD")

        self.currency_menu = OptionMenu(self.win, self.currency_var, "USD", "EUR")
        self.currency_menu.grid(row=2, column=1)

        self.price_label = Label(self.win, text="Rate Bought")
        self.price_label.grid(row=3, column=0)

        self.price_var = StringVar()
        self.price_input = Entry(self.win,textvariable=self.price_var)
        self.price_input.grid(row=3, column=1)

        self.save_button = Button(self.win, text="Save")
        self.save_button.grid()

    def create_edit_popup(self, investment,db):
        if self.popup_is_displayed():
            return

        self.win = Toplevel()
        self.win.wm_title("Edit Investment")
        self.win.focus_set()

        self.win.grab_set()

        self.win.transient(self.frame)
        self.coin_label = Label(self.win, text="Coin Symbol")
        self.coin_label.grid(row=0, column=0)

        self.coin_symbol = Label(self.win, text=investment[1])
        self.coin_symbol.grid(row=0, column=1)

        self.amount_label = Label(self.win, text="Amount")
        self.amount_label.grid(row=1, column=0)

        self.price_var = StringVar()
        self.price_var.set(investment[4])
        self.price_input = Entry(self.win, textvariable=self.price_var)
        self.price_input.grid(row=2, column=1)

        self.amount_var = StringVar()
        self.amount_var.set(investment[3])
        self.amount_input = Entry(self.win, textvariable=self.amount_var)
        self.amount_input.grid(row=1, column=1)

        self.price_label = Label(self.win, text="Rate Bought("+self.currency_symbols[investment[5]]+")")

        self.price_label.grid(row=2, column=0)



        self.update_button = Button(self.win, text="Update",command=lambda: self.update_investment(investment,db))
        self.update_button.grid(row=3,column=0)

        self.delete_button = Button(self.win, text="Delete", command=lambda: self.delete_investment(investment,db))
        self.delete_button.grid(row=3,column=1)

        self.cancel_button = Button(self.win, text="Cancel", command=self.close_window)
        self.cancel_button.grid(row=3,column=2)

    def update_investment(self,investment,db):
        db.update_investment(investment,self.amount_var.get(),self.price_var.get())
        self.load_investments(db)
        self.close_window()

    def delete_investment(self,investment,db):


        db.delete_investment(investment[0])
        self.load_investments(db)
        self.close_window()

    def close_window(self):
        self.win.destroy()



    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))


    def load_investments(self,db):
        self.investments = db.get_investments()


        for child in self.canvas_frame.winfo_children():
            child.destroy()

        self.frames=[]
        self.canvas.config(width=500, height=(30* len(self.investments)))
        i=0
        for inv in self.investments:
            row_frame = Frame(self.canvas_frame,name=str(i))
            #row_frame = Frame(self.canvas_frame,name=str(i),bg="green")
            row_frame.pack(fill=X)
            name_label = Label(row_frame, text=inv[2], width=10, font="-size 15",name=("n,"+str(i)))
            name_label.pack(side=LEFT)
            coin_value = (db.get_coin_value(inv[2]))
            value_color="orange"
            value="{0:.2f}".format( coin_value * inv[3])
            value_bought="{0:.2f}".format( inv[3] * inv[4])

            gain = "{0:.2f}".format((float(value) - float(value_bought)))+self.currency_symbols[inv[5]]
            if float(value)>float(value_bought):
                value_color="green"
            elif float(value)<float(value_bought):
                value_color="red"


            value = (value) + self.currency_symbols[inv[5]]
            value_label = Label(row_frame, width=10, fg=value_color,text=value,name=("v,"+str(i)))
            value_label.pack(side=LEFT)

            gain_label = Label(row_frame, width=10, fg=value_color, text=gain, name=("g," + str(i)))
            gain_label.pack(side=LEFT)
            amount = "{0:.4f}".format(float(inv[3]) )
            amount_label = Label(row_frame, width=10, text=inv[3],name=("a,"+str(i)))
            amount_label.pack(side=LEFT)
            coin_label = Label(row_frame, width=10, text=coin_value,name=("c,"+str(i)))
            coin_label.pack(side=LEFT)
            name_label.bind("<Button-1>", lambda event: self.click_investment(event,db))
            value_label.bind("<Button-1>", lambda event: self.click_investment(event,db))
            amount_label.bind("<Button-1>", lambda event: self.click_investment(event,db))
            coin_label.bind("<Button-1>", lambda event: self.click_investment(event,db))
            i += 1

    def click_investment(self,event,db):
        row=int(str(event.widget).split(",")[-1])
        print("clicked :",self.investments[row])
        self.create_edit_popup(self.investments[row],db)

class Controller:
    def __init__(self):
        self.database = Database("lite.db")
        self.api=API(self.database)
        self.root = Tk()
        self.view = View(self.root,self.database.get_number_of_investments()+1)
        self.view.load_investments(self.database)
        self.view.add_button.bind("<Button>", lambda *args: (self.view.create_popup(*args), self.popup_bind(args[0],self.database)))
        self.view.reload_button.bind("<Button>", lambda event: self.reload(event))




    def popup_bind(self,event,db):
        self.view.save_button.bind("<Button>",lambda event: (self.view.add_investment(event, db) ,self.reload(event)))

    def reload(self,event):
        self.view.create_loading_popup()

        self.api.refresh_coins(self.database)
        self.view.load_investments(self.database)
        self.view.close_window()



    def run(self):
        self.root.title("My Investment")
        self.root.deiconify()
        self.root.mainloop()

    def clear(self, event):
        self.view.ax0.clear()
        self.view.fig.canvas.draw()


if __name__ == '__main__':
    c = Controller()
    c.run()
