from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "supersecretkey"  

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Bhavesh23',
            database='outfitme_db'
        )
        if connection.is_connected():
            print("Connected to MySQL")
        return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    conn = create_connection()
    if conn is None:
        flash("Database connection failed!")
        return redirect(url_for('login_page'))
    
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        flash(f"Welcome back, {user['name']}!")
        return redirect(url_for('landing_page'))  
    else:
        flash("Invalid login credentials!")
        return redirect(url_for('login_page'))

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    conn = create_connection()
    if conn is None:
        flash("Database connection failed!")
        return redirect(url_for('login_page'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("Email already exists. Please use a different email.")
        else:
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, password))
            conn.commit()
            flash("Signup successful! Please log in.")
    except mysql.connector.Error as err:
        flash(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('login_page'))

@app.route('/landingpage.html')
def landing_page():
    return render_template('landingpage.html')

@app.route('/shopping.html')
def shopping_page():
    return render_template('shopping.html')

@app.route('/cart')
def cart_page():
    return render_template('cart.html')

if __name__ == '__main__':
    app.run(debug=True)
