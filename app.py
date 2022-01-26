import sqlite3
from unittest import result
from flask import Flask, redirect, request
from flask import render_template
from BlockChain import BlockChain
from flask import g
import sqlite3 as sql
from flask import url_for

DATABASE = 'tomcoin.db'

app = Flask ("BritCoin server")

blockchain = BlockChain()


def getDB():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_databse', None)
    if db is not None:
        db.close()

@app.route('/')
def homepage():
    return render_template('index.html' )

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/checkacc', methods=['POST', 'GET'])
def checkAccount():
    if request.method == 'POST':
        con = sql.connect(DATABASE)

        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select * from users")
        rows = cur.fetchall()

        username = request.form['uName']
        password = request.form['pw']

        msg = f'cannot find username {username}'

        for row in rows:
            if row['username'] == username:
                account = row
                if account['password'] == password:
                    # msg = f"found account. Hello {row['firstname']}!"
                    return redirect(url_for('userPage', username=account['username']))
                else:
                    msg = f"incorrect password for {row['username']}"
        con.close()
        
        return render_template('result.html', input = msg)

@app.route('/user/<username>')
def userPage(username):
    con = sql.connect(DATABASE)

    con.row_factory = sql.Row

    cur = con.cursor()
    
    cur.execute(f"SELECT * FROM users WHERE username='{username}'")
    account = cur.fetchall()[0]

    cur.execute(f"SELECT username FROM users")
    users = cur.fetchall()
    con.close()


    return render_template('accountPage.html', user = account, bcinput = blockchain, userList = users)

@app.route('/createAccount')
def createAccount ():
    return render_template('createAccount.html')

@app.route('/transaction', methods=['POST', 'GET'])
def createTransaction():
    if request.method == 'POST':
        sender = request.form['user']
        receiver = request.form['receiver']
        amount = int(request.form['amount'])
        
        con = sql.connect(DATABASE)

        con.row_factory = sql.Row

        cur = con.cursor()
        
        cur.execute(f"SELECT * FROM users WHERE username='{sender}'")
        senderAccount = cur.fetchall()[0]
        senderSignature = senderAccount[6]
        # senderBalance = senderAccount[5]

        con.close()

        # cur.execute(f"SElECT * FROM users WHERE username='{receiver}'")
        # receiverAccount = cur.fetchall()[0]
        # receiverBalance = receiverAccount[5]

        # newSenderBalance = senderBalance - amount
        # newReceiverBalance = receiverBalance + amount
        # cur.execute(f"UPDATE users SET balance={newSenderBalance} WHERE username='{sender}'")
        # cur.execute(f"UPDATE users SET balance={newReceiverBalance} WHERE username='{receiver}'")
        # con.commit()
        # print(sender, receiver, amount, senderSignature)

        blockchain.addTransaction(sender, receiver, amount, senderSignature, senderSignature)

        return redirect(url_for('userPage', username=sender))

@app.route('/addrec', methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            fName = request.form['fName']
            lName = request.form['lName']
            uName = request.form['uName']
            email = request.form['email']
            pw = request.form['pw']
            pw2 = request.form['pw2']
            pubKey = blockchain.generateKeys()

            with sql.connect(DATABASE) as con:
                if pw == pw2:
                    cur = con.cursor()
                    cur.execute("INSERT INTO users(username, password, email, firstname, lastname, balance, publicKey) VALUES(?,?,?,?,?,?,?)", (uName, pw, email, fName, lName, 50, pubKey))
                    con.commit()
                    msg = "Record added successfully"
                else:
                    msg = "Passwords did not match"

        except:
            con.rollback()
            msg = "Error inserting information"

        finally:
            con.close()
            return render_template("result.html", input = msg)

@app.route('/mine/<currentUser>', methods = ['POST', 'GET'])
def mineBlock(currentUser):
    
    blockchain.minePendingTransactions(currentUser)
    return redirect(url_for('userPage', username=currentUser))