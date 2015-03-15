#coding=utf-8
import os
import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,Config

from werkzeug import secure_filename

app = Flask(__name__)

app.config.update({'database':os.path.join(app.root_path,'flaskblog.db'),
                   'debug':True,
                   'SECRET_KEY':'development key',
                   'username':'huangnauh',
                   'password':'huangnauh'
                   })

def connect_db():
    conn = sqlite3.connect(app.config['database'])
    conn.row_factory = sqlite3.Row
    #通过字典而不是元组访问行
    return conn
    
def get_db_conn():
    if not hasattr(g,'sqlite_conn'):
        print 'get_db'
        g.sqlite_conn = connect_db()
    return g.sqlite_conn
    
def init_db():
    with app.app_context():
        conn = get_db_conn()
        with app.open_resource('schema.sql','r') as f:
            cursor = conn.cursor()
            cursor.executescript(f.read())
            cursor.close()
            conn.commit()
        
@app.teardown_appcontext
def close(exception):
    if hasattr(g,'sqlite_conn') is not None:
        g.sqlite_conn.close()
        
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404
        
@app.route('/')
def show_entries():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('select title,path from entries order by id desc')
    pages = cur.fetchall()
    return render_template('index.html',pages=pages)

@app.route('/pages/<path:path>/')
def page(path):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('select title,text from entries where path=?',(path,))
    result = cur.fetchall()
    if len(result) == 1:
        return render_template('page.html', page=result[0])
    else:
        return redirect(url_for('page_not_found'))
        
        
    
@app.route('/add',methods=['GET','POST'])
def add_entry():
    if request.method == 'GET':
        return render_template('add.html')
    if not session.get('logged_in'):
        abort(401)
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('insert into entries (title, text,path) values (?,?,?)',[request.form['title'],request.form['text'],request.form['path']])
    cursor.close()
    conn.commit()
    return redirect(url_for('show_entries'))
    
@app.route('/login',methods=['GET','POST'])
def login():
    session['logged_in'] = False
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['username']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['password']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html',error=error)

@app.route('/logout')    
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
    
    
    
        
        
if __name__ == '__main__':
#    init_db()
    app.run(debug=True)           
                   
