from cgitb import text
from tkinter import *
from tkinter import ttk

from pip import main
from BlockChain import BlockChain

import sqlite3

con = sqlite3.connect('tomcoin.db')

cur = con.cursor()


blockchain = BlockChain()

key = blockchain.generateKeys()

# def calculate(*args):
#     try:
#         value = float(feet.get())
#         meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
#     except ValueError:
#         pass

def openLogin():
    username = StringVar()
    usernameEntry = ttk.Entry(mainframe, width=20, textvariable=username)
    usernameEntry.grid(column=1, row=1, sticky=(W, E))
    
    password = StringVar()
    passwordEntry = ttk.Entry(mainframe, width=20, textvariable=password)
    passwordEntry.grid(column=1, row=2, sticky=(W, E))

def openCreateAccount():
    username = StringVar()
    usernameEntry = ttk.Entry(mainframe, width=20, textvariable=username)
    usernameEntry.grid(column=1, row=1, sticky=(W, E))

    email = StringVar()
    emailEntry = ttk.Entry(mainframe, width=20, textvariable=email)
    emailEntry.grid(column=1, row=2, sticky=(W, E))

    password = StringVar()
    passwordEntry = ttk.Entry(mainframe, width=20, textvariable=password)
    passwordEntry.grid(column=1, row=3, sticky=(W, E))

    retypePassword = StringVar()
    retypePasswordEntry = ttk.Entry(mainframe, width=20, textvariable=retypePassword)
    retypePasswordEntry.grid(column=1, row=4, sticky=(W, E))


root = Tk()
root.title("TomCoin")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

# login
loginButon = ttk.Button(mainframe, text="Login", command=openLogin)
createAccountButton = ttk.Button(mainframe, text="Create Account", command=openCreateAccount)

# ttk.Label(mainframe, text="Sender").grid(column=1, row=1, sticky=(W, E))
# ttk.Label(mainframe, text="Receiver").grid(column=1, row=2, sticky=(W, E))
# ttk.Label(mainframe, text="Amount").grid(column=1, row=3, sticky=(W, E))

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)


# feet_entry.focus()
# root.bind("<Return>", calculate)

root.mainloop()