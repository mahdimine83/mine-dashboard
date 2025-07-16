import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Function to create the database and table
def init_db():
    conn = sqlite3.connect('contracts.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY,
            client_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

def get_db_connection():
    conn = sqlite3.connect('contracts.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    contracts = conn.execute('SELECT * FROM contracts').fetchall()
    conn.close()
    return render_template('index.html', contracts=contracts)

@app.route('/add', methods=('GET', 'POST'))
def add_contract():
    if request.method == 'POST':
        client_name = request.form['client_name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        amount = request.form['amount']
        status = request.form['status']

        conn = get_db_connection()
        conn.execute('INSERT INTO contracts (client_name, start_date, end_date, amount, status) VALUES (?, ?, ?, ?, ?)',
                     (client_name, start_date, end_date, amount, status))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_contract.html')

@app.route('/edit/<int:contract_id>', methods=('GET', 'POST'))
def edit_contract(contract_id):
    conn = get_db_connection()
    contract = conn.execute('SELECT * FROM contracts WHERE id = ?', (contract_id,)).fetchone()
    conn.close()

    if request.method == 'POST':
        client_name = request.form['client_name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        amount = request.form['amount']
        status = request.form['status']

        conn = get_db_connection()
        conn.execute('UPDATE contracts SET client_name = ?, start_date = ?, end_date = ?, amount = ?, status = ? WHERE id = ?',
                     (client_name, start_date, end_date, amount, status, contract_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit_contract.html', contract=contract)

if __name__ == '__main__':
    app.run(debug=True)
