import os
from flask import Flask, session, g, render_template, request
from flask.helpers import flash, send_from_directory, url_for 
from werkzeug.utils import redirect
from urllib.parse import urlparse
from flask_bootstrap import Bootstrap
from forms import LoginForm , UploadForm


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'Very Hard Secret'
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')


@app.before_request
def get_name():
    g.name = request.args.get('name')

@app.route('/')
def index():
    user = session.get('username')
    return render_template('index.html', user=user)     

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


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        session['username'] = username
        flash("登录成功，%s！" % username)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

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
        return render_template('needlogin.html')       

def check_next(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(target)
    return ref_url.netloc == test_url.netloc


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = f.filename
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('上传图片文件成功！')
        session['filename'] = filename        
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)

@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')  

if __name__  == '__main__':
    app.run(debug = True)