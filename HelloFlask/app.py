from flask import Flask, session, g, render_template
from flask.helpers import url_for 
from flask import request
from werkzeug.utils import redirect
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/hello')
def hello():
    return '<h1>hello Flask<h1>' 

@app.route('/user/',defaults ={'name': 'pythontxt'})
@app.route('/user/<name>')
def welcome(name):
    res = '<h1>Hello,%s!</h1>' % name
    if 'loginID' in session:
        res += 'Authenticated'
    else:
        res += 'UnAuthenticated'
    return res
    
@app.route('/test/')
def test_view():
    query = 'Flask'
    if request.args:
        query = request.args.get('name', 'Flask')
    host = request.host
    path = request.full_path
    cookie = request.cookies
    method = request.method
    return """
    <h1>
    <p>query string: %s</p>
    <p>host: %s</p>
    <p>path: %s</p>
    <p>cookies: %s</p>
    <p>method: %s</p>
    </h1>
    """ % (query, host, path, cookie, method)

app.secret_key = 'Very Hard Secret'

@app.before_request
def get_name():
    g.name = request.args.get('name')

@app.route('/login')
def login():
    session['loginID'] = 'admin'
    target = request.args.get('next')
    if check_next(target):
        return redirect(target)
    return redirect(url_for('hello'))

@app.route('/logout/')
def logout():
    if 'loginID' in session:
        session.pop('loginID')
    return redirect(url_for('welcome'))

@app.route('/needlogin1/')
def needLogin1():
    if 'loginID' in session:
        user = 'needlogin1'
        return  render_template('hello.html', user = user)
    else:
        return render_templater('needlogin.html')

def check_next(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(target)
    return ref_url.netloc == test_url.netloc

if __name__  == '__main__':
    app.run(debug = True)