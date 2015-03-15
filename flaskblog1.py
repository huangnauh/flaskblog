#coding=utf-8
import os
from datetime import datetime
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,Config
from flask.ext.stormpath import (
    StormpathError,
    StormpathManager,
    User,
    login_required,
    login_user,
    logout_user,
    user,
)
app = Flask(__name__)

app.config.update({'DEBUG':True,
                   'SECRET_KEY':'development key',
                   })
app.config['STORMPATH_API_KEY_FILE'] = os.path.join(app.root_path,'apiKey.properties')
app.config['STORMPATH_APPLICATION'] = 'flaskblog'

stormpath_manager = StormpathManager(app)

        
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404
        
@app.route('/')
def show_entries():
    pages = []
    for account in stormpath_manager.application.accounts:
        if account.custom_data.get('pages'):
            pages.extend(account.custom_data['pages'])
    pages = sorted(pages, key=lambda k: k['date'], reverse=True)    
    return render_template('index1.html',pages=pages)

@app.route('/pages/<path:path>/')
def page(path):
    result = None
    for account in stormpath_manager.application.accounts:
        if account.custom_data.get('pages'):
            for page in account.custom_data['pages']:
                if page['path'] == path:
                    result = page
                    break
    if result is not None:
        return render_template('page1.html', page=result)
    else:
        return redirect(url_for('page_not_found'))
        
        
    
@app.route('/add',methods=['get','POST'])
@login_required
def add_entry():
    if request.method == 'GET':
        return render_template('add.html')
    if not user.custom_data.get('pages'):
        user.custom_data['pages'] = []
    user.custom_data['pages'].append({
        'date':datetime.utcnow().isoformat(),
        'title':request.form['title'],
        'text': request.form['text'],
        'path': request.form['path'],
        })
    user.save()
    return redirect(url_for('show_entries'))
    
@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            _user = User.from_login(
                request.form['email'],
                request.form['password'],
                )
            login_user(_user,remember=True)
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        except StormpathError, err:
            error = err.message
    return render_template('login1.html',error=error)

@app.route('/logout')    
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('show_entries'))
    
    
    
        
        
if __name__ == '__main__':
    app.run(debug=True)           
                   
