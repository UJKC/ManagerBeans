from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '',
    'host': 'localhost',  # Use Docker container's IP address or hostname
    'port': '5432'        # PostgreSQL default port
}

# Database connection function
def connect_to_db():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL database:", e)
        return None

# Route to fetch data from database
@app.route('/dash')
def get_data():
    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        cur.close()
        conn.close()
        return "Connected"
    else:
        return "Failed to connect to database"
    
@app.route('/dashback/employeeinfo')
def get_indexinfo():
    buffer = []
    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        cur.execute("select path, EmployeeID, FullName, JobTitle, OfficeLocation, Email, PhoneNumber from Employee Natural join WorkInformation;")
        rows = cur.fetchall()
        for row in rows:
            appender = {
                'path': row[0],
                'EmployeeID': row[1],
                'name': row[2],
                'work': row[3],
                'location': row[4],
                'email': row[5],
                'phone': row[6]
            }
            buffer.append(appender)
        cur.close()
        conn.close()
        print(buffer)
        return jsonify(buffer)
    else:
        return "Failed to connect to database"

if __name__ == '__main__':
    app.run(debug=True)
