# server.py
import time
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
DELAYSIM = 0.5

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
    time.sleep(DELAYSIM)
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Missing username or password"})

    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()

    if user:
        uid, username, password, displayname = user
        session['user_id'] = uid  # Store user ID in session
        session['username'] = username
        session['displayname'] = displayname
        return jsonify({
            "success": True,
            "user": {
                "id": uid,
                "name": displayname
            }
        })
    else:
        return jsonify({"success": False, "message": "Invalid username or password"})

@app.route('/check_session', methods=['GET'])
def check_session():
    time.sleep(DELAYSIM)
    if 'user_id' in session:
        return jsonify({
            "success": True,
            "user": {
                "id": session['user_id'],
                "name": session['displayname']
            }
        })
    else:
        return jsonify({"success": False, "message": "No active session"})

@app.route('/logout', methods=['POST'])
def logout():
    time.sleep(DELAYSIM)
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully"})

if __name__ == '__main__':
    app.run(port=6310, debug=True)