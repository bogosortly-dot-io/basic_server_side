from flask import Flask, session, redirect, url_for, request
import sqlite3
from hashlib import sha256
from markupsafe import escape

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return 'You are not logged in'

    if request.method == 'POST':
        #check login exists
        con = sqlite3.connect('finsta_db')
        cur = con.cursor()
        cur.execute("INSERT INTO notes VALUES (?, ?)", (session['username'], request.form['new_note']))
        con.commit()
        con.close()

        return redirect(url_for('index'))

    con = sqlite3.connect('finsta_db')
    cur = con.cursor()
    notes = cur.execute("SELECT text FROM notes WHERE creator = ?", (session['username'],)).fetchall()
    con.commit()
    con.close()

    notes_string = build_notes_string(notes)
    return '<form method="post"><p><input type=text name=new_note></p><p><input type=submit value=NewNote></p></form><h1> all your notes, ' + session['username'] +' ;)</h1>' + notes_string


def build_notes_string(notes_db_results):
    notes_string = ""
    for result in notes_db_results:
        result_string = result[0]
        p_tag = "<p>" + result_string + "</p>"
        notes_string += p_tag

    return notes_string

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #check login exists
        con = sqlite3.connect('finsta_db')
        cur = con.cursor()
        results = cur.execute('SELECT * FROM users WHERE username = ? and password = ?', (request.form['username'], request.form['password'])).fetchall()
        con.commit()
        con.close()
        if len(results) == 0:
            return "Heyyy, that user does not exist. go to the signup page ;)"

        #log in the person
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # check username not taken

        # check passwords match

        # add new user to users database
        con = sqlite3.connect('finsta_db')
        cur = con.cursor()
        cur.execute("INSERT INTO users VALUES (?, ?)", (request.form['username'], request.form['password']))
        con.commit()
        con.close()

        #login as new account
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=text name=confirm_password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
