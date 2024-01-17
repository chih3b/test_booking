from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Admin view to display all users and their bookings
@app.route('/')
@app.route('/admin')
def admin():
    conn = sqlite3.connect('travel_db.sqlite')
    cursor = conn.cursor()

    # Fetch all users
    cursor.execute('SELECT DISTINCT client_name FROM bookings')
    users = cursor.fetchall()

    # Fetch all bookings
    cursor.execute('SELECT client_name, destination, travel_date FROM bookings')
    bookings = cursor.fetchall()

    conn.close()

    return render_template('admin.html', users=users, bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True,port=5001)
