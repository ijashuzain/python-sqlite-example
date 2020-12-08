from flask import *
import sqlite3
from flask.templating import render_template
from werkzeug import useragents

app = Flask(__name__)
app.secret_key = "vbngh"

# conn = sqlite3.connect('database.db')
# conn.execute('CREATE TABLE students (name TEXT, username TEXT, password TEXT)')
# conn.close()

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('home.html', name=username)
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM students WHERE username='" +
                    username + "' AND password='" + password +"'")

        rows = cur.fetchone()
        
        # name = rows["name"]
        # session['username'] = rows["name"]
    

        if rows is not None:
            session['username'] = rows["name"]
            return redirect(url_for('index'))        
        else:
            return render_template('login.html')

@app.route('/enternew')
def new_student():
    if 'username' in session:
        return render_template('student.html')
    else:
        return redirect(url_for('index'))

@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            usr = request.form['user']
            pwd = request.form['pass']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO students (name,username,password) VALUES(?,?,?)", (nm, usr, pwd))
                con.commit()
                msg = "Record Added Successfully"
                
        except:
            con.rollback()
            msg = "Error in Insertion"

        finally:
            con.close()
            return render_template("result.html", msg=msg)


@app.route('/list')
def list():
    if 'username' in session:
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM students")

        rows = cur.fetchall()
        return render_template("list.html", rows=rows)
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
