from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '',
    'host': 'webapp-postgres',  # Use Docker container's IP address or hostname
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
@app.route('/dashback')
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
    
@app.route('/dashback/recieveai', methods=['POST'])
def dashback():
    # Get the data from the request
    data = request.json
    print(data)

    # Process the data as needed
    # For example, you can log it or perform further operations
    
    # Return a response if necessary
    return jsonify({"status": "success", "message": "Data received successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
