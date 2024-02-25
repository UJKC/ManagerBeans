from flask import Flask, jsonify
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)

def check_postgres_connection():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="",
            host="webapp-postgres"
        )
        conn.close()
        return True
    except OperationalError:
        return False

# Route for checking PostgreSQL connection status
@app.route('/auth/connection-status')
def connection_status():
    if check_postgres_connection():
        return jsonify({'status': 'PostgreSQL connection is OK'})
    else:
        return jsonify({'status': 'Failed to connect to PostgreSQL'})

# Route for login/authentication
@app.route('/auth/login', methods=['POST'])
def login():
    # Authentication logic goes here
    return 'Login page'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
