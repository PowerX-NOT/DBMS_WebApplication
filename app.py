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
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        return render_template('table_list.html', db_name=db_name, tables=tables, user=user, password=password)
    except mysql.connector.Error as err:
        flash(f"Error: {err}")
        return redirect(url_for('login_page'))

@app.route('/table/<table_name>', methods=['POST'])
def table_actions(table_name):
    db_name = request.form['db_name']
    user = request.form['user']
    password = request.form['password']
    action = request.form['action']

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=db_name
        )
        cursor = conn.cursor()

        if action == "view_data":
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return render_template('view_data.html', table_name=table_name, columns=columns, rows=rows)

        elif action == "add_data":
            # Render form for adding data
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [col[0] for col in cursor.fetchall()]
            return render_template('add_data.html', table_name=table_name, columns=columns, db_name=db_name, user=user, password=password)

        elif action == "update_data":
            # Render form for updating data
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [col[0] for col in cursor.fetchall()]
            return render_template('update_data.html', table_name=table_name, columns=columns, db_name=db_name, user=user, password=password)

        elif action == "delete_data":
            # Render form for deleting data
            return render_template('delete_data.html', table_name=table_name, db_name=db_name, user=user, password=password)

    except mysql.connector.Error as err:
        flash(f"Error: {err}")
        return redirect(url_for('use_database'))

@app.route('/add_data/<table_name>', methods=['POST'])
def add_data(table_name):
    db_name = request.form['db_name']
    user = request.form['user']
    password = request.form['password']
    data = {key: request.form[key] for key in request.form if key not in ['db_name', 'user', 'password']}

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=db_name
        )
        cursor = conn.cursor()
        columns = ', '.join(data.keys())
        values = ', '.join([f"'{value}'" for value in data.values()])
        cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
        conn.commit()
        flash("Data added successfully.")
        return redirect(url_for('use_database'))
    except mysql.connector.Error as err:
        flash(f"Error: {err}")
        return redirect(url_for('use_database'))

@app.route('/update_data/<table_name>', methods=['POST'])
def update_data(table_name):
    db_name = request.form['db_name']
    user = request.form['user']
    password = request.form['password']
    update_column = request.form['update_column']
    update_value = request.form['update_value']
    condition = request.form['condition']

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=db_name
        )
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {table_name} SET {update_column} = '{update_value}' WHERE {condition}")
        conn.commit()
        flash("Data updated successfully.")
        return redirect(url_for('use_database'))
    except mysql.connector.Error as err:
        flash(f"Error: {err}")
        return redirect(url_for('use_database'))

@app.route('/delete_data/<table_name>', methods=['POST'])
def delete_data(table_name):
    db_name = request.form['db_name']
    user = request.form['user']
    password = request.form['password']
    condition = request.form['condition']

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=db_name
        )
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
        conn.commit()
        flash("Data deleted successfully.")
        return redirect(url_for('use_database'))
    except mysql.connector.Error as err:
        flash(f"Error: {err}")
        return redirect(url_for('use_database'))

if __name__ == '__main__':
    app.run(debug=True)
