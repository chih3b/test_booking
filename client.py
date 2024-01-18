from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Database initialization
def init_db():
    conn = sqlite3.connect('travel_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            destination TEXT,
            travel_date TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home page with travel offers
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
    else:
        username = None

    travel_offers = [
        {'destination': 'Oases of Tamerza, Chebika, and Midès', 'price': '$80', 'image': 'tamerza_chebika_mides.jpg'},
        {'destination': 'Onk Jemel', 'price': '$78.76', 'image': 'onk_jemel.jpg'},
        {'destination': 'Chott el Djerid', 'price': '$115.00', 'image': 'chott_el_djerid.jpg'},
        {'destination': 'Ouled Hadef', 'price': '$62.50', 'image': 'ouled_hadef.jpg'},
        # Add more travel offers
    ]
    return render_template('index.html', travel_offers=travel_offers, username=username)

# Booking form submission
@app.route('/book', methods=['POST'])
def book():
    if request.method == 'POST':
        client_name = request.form['client_name']
        destination = request.form['destination']
        travel_date = request.form['travel_date']

        conn = sqlite3.connect('travel_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bookings (client_name, destination, travel_date) VALUES (?, ?, ?)',
                       (client_name, destination, travel_date))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Use the correct hashing method
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = sqlite3.connect('travel_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        flash('Signup successful! Please login.')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('travel_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.')

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
