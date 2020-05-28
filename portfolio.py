import requests
import json
from tkinter import *
from tkinter import messagebox , Menu
import sqlite3

#Tkinter
cyrpto = Tk()
cyrpto.title("My Cyrpto Portfolio")
cyrpto.iconbitmap("Fasticon1.ico")

#database 
c = sqlite3.connect("coins.db")
co = c.cursor()
co.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY , symbol TEXT , price REAL , owned INTEGER)")
c.commit()

#reloading the window again
def reset():
    for cell in cyrpto.winfo_children():
        cell.destroy()
    app_nav()
    app_header()
    my_portfolio()
# navigation bar
def app_nav():

    def clear_all():
        co.execute("DELETE FROM coin")
        c.commit()
        reset()
        messagebox.showinfo("Portfolio Notification","Portfolio Cleared ----- Add new coins")
    def close_app():
        cyrpto.destroy()
    def about():
        messagebox.showinfo("about us","This application is Developed by Yatharth Sharma    # Technologies used # 1) Python  2) sqlite3  3) Tkinter 4) Coinmarketcap API")    

    menu= Menu(cyrpto)
    file_item=Menu(menu)
    file_item.add_command(label='Clear Portfolio', command= clear_all)
    file_item.add_command(label='Close Application', command=close_app)
    file_item.add_command(label='About Us', command=about)
    menu.add_cascade(label="File",menu=file_item)
    cyrpto.config(menu=menu)
    
# main fxn
def my_portfolio():

    api_request=requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=100&convert=USD&CMC_PRO_API_KEY=a5945a66-4e06-44f6-8017-1a1e7652e206")
    api= json.loads(api_request.content)    #parsing json data to python object //result is a python dictionary

    def font_color(test):
        if test>=0:
            return "green"
        else:
            return "red"

    def insert_coin():
        co.execute("INSERT INTO coin(symbol , price , owned) VALUES(?,?,?)",(symbol_txt.get(),price_txt.get(),owned_txt.get()))
        c.commit()
        reset()
        messagebox.showinfo("Portfolio Notification "," Coin Added Successfully")

    def update_coin():
        co.execute("UPDATE coin SET symbol=? , price=? , owned=? WHERE id=? ",(symbol_update.get(),price_update.get(),owned_update.get(),id_update.get()))
        c.commit()
        reset()
        messagebox.showinfo("Portfolio Notification "," Coin Updated Successfully")

    def delete_coin():
        co.execute("DELETE FROM coin WHERE id=? ",(id_delete.get(),))
        c.commit()
        reset()
        messagebox.showinfo("Portfolio Notification "," Coin Deleted Successfully")

    co.execute("SELECT * FROM coin")
    coins = co.fetchall()

    overall_pl=0
    coin_row=1
    tcv=0
    tvi=0

    for i in range(0,100):

        for coin in coins:

            if coin[1] == api["data"][i]["symbol"]:

                total_invst_val = coin[2] * coin[3]
                total_curr_val = coin[3] * api["data"][i]["quote"]["USD"]["price"]
                pl_per_coin = api["data"][i]["quote"]["USD"]["price"] - coin[2]
                total_pl = pl_per_coin * coin[3]

                overall_pl += total_pl
                tvi += total_invst_val
                tcv += total_curr_val

                Portfolio_ID = Label( cyrpto , text=coin[0] , bg="#F3F4F6", fg='black', font="Lato 10 ", padx="2", pady="2",borderwidth=2, relief="groove")
                Portfolio_ID.grid(row=coin_row, column=0, sticky=N+S+E+W )

                name = Label( cyrpto , text=api["data"][i]["symbol"] , bg="#F3F4F6", fg='black', font="Lato 10 ", padx="2", pady="2",borderwidth=2, relief="groove")
                name.grid(row=coin_row, column=1, sticky=N+S+E+W )

                price = Label( cyrpto , text=coin[2] , bg="#F3F4F6", fg='black', font="Lato 10 ", padx="2", pady="2",borderwidth=2, relief="groove")
                price.grid(row=coin_row, column=2, sticky=N+S+E+W )

                no_coins = Label( cyrpto , text= "{0:.2f} ". format(coin[3]) , bg="#F3F4F6", fg='black', font="Lato 10 ", padx="2", pady="2",borderwidth=2, relief="groove")
                no_coins.grid(row=coin_row, column=3, sticky=N+S+E+W )

                amount_paid = Label( cyrpto , text=" {0:.2f} ".format(total_invst_val) , bg="#F3F4F6", fg='black', font="Lato 10 ", padx="2", pady="2",borderwidth=2, relief="groove")
                amount_paid.grid(row=coin_row, column=4, sticky=N+S+E+W )

                current_value = Label( cyrpto , text=" {0:.2f} ".format(total_curr_val) , bg="#F3F4F6", fg =font_color(float(" {0:.2f} ".format(total_curr_val))), font="Lato 10 ", padx="2", pady="2",borderwidth=2, relief="groove")
                current_value.grid(row=coin_row, column=5, sticky=N+S+E+W )

                pl_coin = Label( cyrpto , text=" {0:.2f}  ".format(pl_per_coin) , bg="#F3F4F6", fg=font_color(float(" {0:.2f} ".format(pl_per_coin))), font="Lato 10 ", padx="2", pady="2",borderwidth=2, relief="groove")
                pl_coin.grid(row=coin_row, column=6, sticky=N+S+E+W )

                totalpl = Label( cyrpto , text=" {0:.2f}  ".format(total_pl) , bg="#F3F4F6", fg=font_color(float(" {0:.2f} ".format(total_pl))), font="Lato 10 ", padx="2", pady="2",borderwidth=2, relief="groove")
                totalpl.grid(row=coin_row, column=7, sticky=N+S+E+W )

                coin_row += 1
    #ADD DATA
    symbol_txt = Entry(cyrpto , borderwidth=2 ,relief="groove")
    symbol_txt.grid(row = coin_row+1 , column=1)

    price_txt = Entry(cyrpto , borderwidth=2 ,relief="groove")
    price_txt.grid(row = coin_row+1 , column=2)

    owned_txt = Entry(cyrpto , borderwidth=2 ,relief="groove")
    owned_txt.grid(row = coin_row+1 , column=3)

    add_coin = Button( cyrpto , text="Add Coin" , bg="#142E54", fg='white', command= insert_coin , font="Lato 13 ",borderwidth=4 ,relief="groove")
    add_coin.grid(row=coin_row +1, column=4, sticky=N+S+E+W )

    #UPDATE data
    id_update = Entry(cyrpto , borderwidth=2 ,relief="groove")
    id_update.grid(row = coin_row+2 , column=0)

    symbol_update= Entry(cyrpto , borderwidth=2 ,relief="groove")
    symbol_update.grid(row = coin_row+2 , column=1)

    price_update = Entry(cyrpto , borderwidth=2 ,relief="groove")
    price_update.grid(row = coin_row+2 , column=2)

    owned_update = Entry(cyrpto , borderwidth=2 ,relief="groove")
    owned_update.grid(row = coin_row+2 , column=3)

    update_coin_txt = Button( cyrpto , text="Update Coin" , bg="#142E54", fg='white', command= update_coin , font="Lato 13 ",borderwidth=4 ,relief="groove")
    update_coin_txt.grid(row=coin_row+2, column=4, sticky=N+S+E+W )

    #delete data
    id_delete = Entry(cyrpto , borderwidth=2 ,relief="groove")
    id_delete.grid(row = coin_row+3 , column=0)

    delete_coin_txt = Button( cyrpto , text="Delete Coin" , bg="#142E54", fg='white', command= delete_coin , font="Lato 13 ",borderwidth=4 ,relief="groove")
    delete_coin_txt.grid(row=coin_row+3, column=4, sticky=N+S+E+W )


    #totaling work
    overall = Label( cyrpto , text="{0:.2f}  ".format(overall_pl) , bg="bisque", fg=font_color(float(" {0:.2f} ".format(overall_pl))), font="Lato 13 bold", padx="5", pady="5",borderwidth=4 ,relief="groove")
    overall.grid(row=coin_row, column=7, sticky=N+S+E+W )

    overalltvi = Label( cyrpto , text="{0:.2f}  ".format(tvi) , bg="grey", fg='black', font="Lato 13 bold", padx="5", pady="5",borderwidth=4 ,relief="groove")
    overalltvi.grid(row=coin_row, column=4, sticky=N+S+E+W )

    overalltcv = Label( cyrpto , text="{0:.2f}  ".format(tcv) , bg="bisque", fg=font_color(float(" {0:.2f} ".format(tcv))), font="Lato 13 bold", padx="5", pady="5",borderwidth=4 ,relief="groove")
    overalltcv.grid(row=coin_row, column=5, sticky=N+S+E+W )

    api = ""

    Refresh = Button( cyrpto , text="Refresh" , bg="#142E54", fg='white', command= reset , font="Lato 13 ",borderwidth=4 ,relief="groove")
    Refresh.grid(row=coin_row +1, column=7, sticky=N+S+E+W )
    
#header off main window
def app_header():

    Portfolio_ID = Label( cyrpto , text="Portfolio_ID" , bg="#142E54", fg='white', font="Lato 12 bold", padx="5", pady="5",borderwidth=2 ,relief="groove")
    Portfolio_ID.grid(row=0, column=0, sticky=N+S+E+W )

    name = Label( cyrpto , text="Coin Name" , bg="#142E54", fg='white', font="Lato 12 bold", padx="5", pady="5",borderwidth=2 ,relief="groove")
    name.grid(row=0, column=1, sticky=N+S+E+W )

    price = Label( cyrpto , text="Price" , bg="#142E54", fg='white', font="Lato 12 bold", padx="5", pady="5",borderwidth=2 ,relief="groove")
    price.grid(row=0, column=2, sticky=N+S+E+W )

    no_coins = Label( cyrpto , text="Coins Owned" , bg="#142E54", fg='white', font="Lato 12 bold", padx="5", pady="5",borderwidth=2 ,relief="groove")
    no_coins.grid(row=0, column=3, sticky=N+S+E+W )

    amount_paid = Label( cyrpto , text="Total Amount Paid" , bg="#142E54", fg='white', font="Lato 12 bold", padx="5", pady="5",borderwidth=2 ,relief="groove")
    amount_paid.grid(row=0, column=4, sticky=N+S+E+W )

    current_value = Label( cyrpto , text="Current Value" , bg="#142E54", fg='white', font="Lato 12 bold", padx="5", pady="5",borderwidth=2 ,relief="groove")
    current_value.grid(row=0, column=5, sticky=N+S+E+W )

    pl_coin = Label( cyrpto , text="P/L Per Coin" , bg="#142E54", fg='white', font="Lato 12 bold", padx="5", pady="5",borderwidth=2 ,relief="groove")
    pl_coin.grid(row=0, column=6, sticky=N+S+E+W )

    totalpl = Label( cyrpto , text="Total P/L With Coin" , bg="#142E54", fg='white', font="Lato 12 bold", padx="5", pady="5",borderwidth=2 ,relief="groove")
    totalpl.grid(row=0, column=7, sticky=N+S+E+W )

app_nav()
app_header()
my_portfolio()
cyrpto.mainloop()
co.close()
c.close()
