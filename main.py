from flask import Flask, render_template, request, redirect, g
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

DATABASE = 'guestbook.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.execute(f.read())
        db.commit()

def get_messages(limit=10):
    db = get_db()
    try:
        cursor = db.execute('SELECT message, timestamp FROM messages ORDER BY timestamp DESC LIMIT ?', (limit,))
        messages = []
        for row in cursor.fetchall():
            # Convert the timestamp string to a proper datetime format for display
            messages.append({
                'message': row[0],
                'timestamp': row[1].strftime('%B %d, %Y at %H:%M')
            })
        return messages
    except sqlite3.OperationalError:
        # If table doesn't exist, create it
        db.execute('''
            CREATE TABLE IF NOT EXISTS messages
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             message TEXT NOT NULL,
             timestamp DATETIME NOT NULL)
        ''')
        db.commit()
        return []

@app.route('/', methods=['GET'])
def home():
    messages = get_messages()
    return render_template('index.html', messages=messages)

@app.route('/sign', methods=['POST'])
def sign():
    message = request.form['message']
    if message:  # Check if the message is not empty
        db = get_db()
        current_time = datetime.utcnow()
        db.execute('INSERT INTO messages (message, timestamp) VALUES (?, ?)',
                  (message, current_time))
        db.commit()
    return redirect('/')

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, host='0.0.0.0', port=8080)