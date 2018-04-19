import os
from flask import Flask, url_for, request, send_from_directory
from flask import render_template, abort, redirect, session, escape, flash
from werkzeug.utils import secure_filename, redirect

app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return 'Hello World!2222___22___1_24'




@app.route('/bye/')
def bye():
    return render_template("bye.html")


@app.route('/user/<username>')
def show_user_profile(username):
    # показать профиль данного пользователя
    # return '%s: Jhon' % username
    return 'User: ' + username


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


UPLOAD_FOLDER = "M:\\Flask\\upload_files"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx'])


# функция возвращает True, если в файле есть точка и расширение входящее в ALLOWED_EXTENSIONS, но это не точно.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/file_loader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


# Сессии
@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # удалить из сессии имя пользователя, если оно там есть
    session.pop('username', None)
    return redirect(url_for('index'))


# Flash-сообщения
@app.route('/index_flash')
def index_flash():
    return render_template('index_flash.html')


@app.route('/login_flash', methods=['GET', 'POST'])
def login_flash():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                        request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index_flash'))
    return render_template('login_flash.html', error=error)


app.route('/layout')
def layout():
    return render_template('layout.html')

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # Ограничение размера файла в 16мб
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    # set the secret key.  keep this really secret:
    app.secret_key = os.urandom(24)
    app.debug = True
    app.run()
