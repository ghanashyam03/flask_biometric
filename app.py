# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# MySQL configurations
db = pymysql.connect(host='localhost',
                     user='root',
                     password='ghanalm10',
                     db='biometric',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

# API endpoint for user signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    try:
        with db.cursor() as cursor:
            # Check if the username already exists
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            result = cursor.fetchone()

            if result:
                return jsonify({'message': 'Username already exists'}), 400

            # If the username is unique, insert the new user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()

            return jsonify({'message': 'Signup successful'}), 201

    except Exception as e:
        print(e)
        return jsonify({'message': 'Error during signup'}), 500

if __name__ == '__main__':
    app.run(debug=True)
