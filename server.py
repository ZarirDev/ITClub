# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize SQLite database
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (uid INTEGER UNIQUE, username TEXT UNIQUE, password TEXT, displayname TEXT)''')
conn.commit()

# Sample user for testing
c.execute("INSERT OR IGNORE INTO users (uid, username, password, displayname) VALUES (?, ?, ?, ?)", (10, 'zarir', 'zarir100', 'Ahmad Zarir'))
conn.commit()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Missing username or password"})

    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()

    if user:
        uid, username, password, displayname = user
        return jsonify({
            "success": True,
            "user": {
                "id": uid,
                "name": displayname
            }
        })
    else:
        return jsonify({"success": False, "message": "Invalid username or password"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)