import flask_bcrypt
from app import app, mysql
from flask import render_template, redirect, url_for, session, request
import MySQLdb.cursors


@app.route('/', methods=["GET", "POST"])
def Register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        h_password = flask_bcrypt.generate_password_hash(password)
        dados = (username, email, h_password)
        query = "INSERT INTO contas (`username`, `email`, `password`)  VALUES (%s, %s, %s)"
        cursor.execute(query, dados)
        mysql.connection.commit()
        print(type(h_password))
        return redirect(url_for("Login"))
    return render_template('register2.html')


@app.route('/login', methods=["GET", "POST"])
def Login():
    if request.method == 'POST' and 'username' in request.form: # and 'password' in request.form:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        username = request.form['username']
        cursor.execute(f"SELECT * FROM contas WHERE username = '{username}'")
        account = cursor.fetchone()
        if flask_bcrypt.check_password_hash(account['password'], request.form['password']):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for("homePage"))
        else:
            return redirect(url_for("Register"))
    return render_template('login2.html')


@app.route('/homepage')
def homePage():
    if 'loggedin' in session:
        return render_template('homepage.html')
    return redirect(url_for('Login'))


@app.route('/tabela-pdfs')
def tabela_pdfs():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM imports")
        data = cursor.fetchall()
        return render_template('pdfs_lidos.html', data=data)

    return redirect(url_for('Login'))


@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('Login'))
