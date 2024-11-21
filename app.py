from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form['username']
    password = request.form['password']

    try:
        # Connect to MySQL with provided credentials
        conn = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password
        )
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        return render_template('database_list.html', databases=databases, user=user, password=password)
    except mysql.connector.Error as err:
        flash(f"Error: {err}")
        return redirect(url_for('login_page'))

@app.route('/use_database', methods=['POST'])
def use_database():
    db_name = request.form['database']
    user = request.form['user']
    password = request.form['password']

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=db_name
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Vehicles")
        vehicles = cursor.fetchall()
        return render_template('vehicles.html', vehicles=vehicles, db_name=db_name)
    except mysql.connector.Error as err:
        flash(f"Error: {err}")
        return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)

