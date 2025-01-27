import time
from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
DELAYSIM = 0
PORTTOHOST=8000

# Initialize SQLite database
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (snid INTEGER PRIMARY KEY, uid INTEGER UNIQUE, email TEXT UNIQUE, password TEXT, displayname TEXT)''')
conn.commit()

# Sample user for testing (this is a comment now as you're shifting to email)
# c.execute("INSERT OR IGNORE INTO users (uid, email, password, displayname) VALUES (?, ?, ?, ?)", (10, 'zarir498@gmail.com', 'zarir100', 'Ahmad Zarir'))
# conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    time.sleep(DELAYSIM)
    data = request.get_json()
    email = data.get('email')  # Updated to email
    password = data.get('password')

    if not email or not password:
        return jsonify({"success": False, "message": "Missing email or password"})

    # Update SQL query to use email instead of username
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()

    if user:
        snid, uid, email, password, displayname = user  # Unpack correctly based on the number of columns
        session['user_id'] = uid  # Store user ID in session
        session['email'] = email  # Store email in session
        session['displayname'] = displayname
        return jsonify({
            "success": True,
            "user": {
                "id": uid,
                "name": displayname
            }
        })
    else:
        return jsonify({"success": False, "message": "Invalid email or password"})

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
    app.run(port=PORTTOHOST, debug=True)