from flask import Flask, render_template, request

import sqlite3

app = Flask(__name__)

def create_connection():
    #Create database
    conn = sqlite3.connect('inventory.db') #Connection object that represents database

    #Create cursor object, call its execute() method to perform SQL commands
    cur = conn.cursor()

    #Account for sqlite3.OperationalError: table already exists
    cur.execute('DROP TABLE IF EXISTS nfts')
    #Create table
    cur.execute('''CREATE TABLE nfts (id INTEGER, name TEXT, image TEXT, price REAL, qty INTEGER)''')

    #Insert NFTs to buy
    cur.executescript('''
    INSERT INTO nfts VALUES (1, 'Serene Forest', 'serene_forest.jpeg', 1.855, 4 );
    INSERT INTO nfts VALUES (2, 'Superpanda', 'super_panda.jpeg', 3.800, 2 );
    INSERT INTO nfts VALUES (3, 'Dreams', 'dreams.png', 0.106, 1 );
    INSERT INTO nfts VALUES (4, 'Miss You Japan', 'Miss You Japan.png', 1.24, 6 );
    ''')

    #Commit changes
    conn.commit()

@app.route('/')
def display_all_nfts():
    conn = sqlite3.connect('inventory.db')
    cur = conn.cursor()
    cur.execute(''' SELECT * FROM nfts ''')
    rows = cur.fetchall()
    print(rows)
    cur.execute(''' SELECT SUM(price) FROM nfts ''')
    return (conn, cur, rows)

def nft_landingpage():
    (conn, cur, rows, sumtotal) = display_all_nfts()
    return render_template("index.html",  rows=rows)

@app.route('/delete/<id>')
def delete(id):
    conn = sqlite3.connect('inventory.db')
    cur = conn.cursor()
    cur.execute(''' DELETE FROM nfts WHERE id = ? ''', (id))
    delete_nft = 'DELETE FROM nfts WHERE id = ' + id
    rows = cur.execute(''' SELECT * FROM nfts ''')
    conn.commit() #deletions are persistent
    return render_template("index.html", rows=rows, delete_nft=delete_nft)

@app.route('/reset')
def reset():
    create_connection()
    (conn, cur, rows) = display_all_nfts()
    return render_template("index.html", rows=rows)

@app.route('/sell/<id>')
def sell(id):
    conn = sqlite3.connect('inventory.db')
    cur = conn.cursor()

    #if an NFT in inventory reaches 0, remove entry from database
    cur.execute(''' SELECT qty FROM nfts WHERE rowid = ? ''', (id))
    access_quantity = cur.fetchone()
    (qty) = access_quantity[0]

    if qty == 1:
        delete(id)

    cur.execute(''' UPDATE nfts SET qty = qty - 1 WHERE rowid = ? ''', (id))
    rows = cur.execute(''' SELECT * FROM nfts ''')
    conn.commit()
    return render_template("index.html", rows = rows)

#navigate to when click 'Edit Price'
@app.route('/edit_price', methods = ['POST', 'GET'])
def price_change():
    if request.method == 'GET':
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        id_no = request.args.get('id_no')
        rows = cur.execute(''' SELECT * FROM nfts WHERE id = ? ''', (id_no))
    return render_template('index.html', rows = rows)

#after updating price, see the change in db
@app.route('/price_change_confirm', methods = ['POST', 'GET'])
def price_confirm():
    if request.method == 'POST':
        id_no = request.form['id_no']
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        price = request.form['price']
        cur.execute(''' UPDATE nfts SET price = ? WHERE id = ?''', (price, id_no))
        rows = cur.execute(''' SELECT * FROM nfts ''')
        conn.commit()
    return render_template('index.html', rows = rows)

@app.route('/edit_quantity', methods = ['POST', 'GET'])
def quant_change():
    if request.method == 'GET':
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        id_no = request.args.get('id_no')
        rows = cur.execute(''' SELECT * FROM nfts WHERE id = ? ''', (id_no))
    return render_template('index.html', rows = rows)

@app.route('/quantity_change_confirm', methods = ['POST', 'GET'])
def quant_confirm():
    if request.method == 'POST':
        id_no = request.form['id_no']
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        qty = request.form['qty']
        cur.execute(''' UPDATE nfts SET qty = ? WHERE id = ?''', (qty, id_no))
        rows = cur.execute(''' SELECT * FROM nfts ''')
        conn.commit()
    return render_template('index.html', rows = rows)

@app.route('/50discount/<id>')
def discount50(id):
    conn = sqlite3.connect('inventory.db')
    cur = conn.cursor()
    cur.execute(''' SELECT price FROM nfts WHERE rowid = ? ''', (id))
    cur.execute(''' UPDATE nfts SET price = price * .5 WHERE rowid = ? ''', (id))
    rows = cur.execute(''' SELECT * FROM nfts ''')
    conn.commit()
    return render_template("index.html", rows = rows)

@app.route('/10discount/<id>')
def discount10(id):
    conn = sqlite3.connect('inventory.db')
    cur = conn.cursor()
    cur.execute(''' SELECT price FROM nfts WHERE rowid = ? ''', (id))
    cur.execute(''' UPDATE nfts SET price = price * .9 WHERE rowid = ? ''', (id))
    rows = cur.execute(''' SELECT * FROM nfts ''')
    conn.commit()
    return render_template("index.html", rows = rows)
    
if __name__ == '__main__':
    app.run(debug=True)