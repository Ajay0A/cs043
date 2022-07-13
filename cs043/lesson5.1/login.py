import wsgiref.simple_server
import urllib.parse
import sqlite3

connection = sqlite3.connect('login5.db')
cursor = connection.cursor()
connection.execute('CREATE TABLE login (username, password)')

def login_app(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8')]

    param = urllib.parse.parse_qs(environ['QUERY_STRING'])
    path = environ['PATH_INFO']
    un = param['username'][0] if 'username' in param else None
    pw = param['password'][0] if 'password' in param else None

    if path == '/register' and un and pw:
        user = cursor.execute('SELECT * FROM login WHERE username = ?', [un]).fetchall()

        if user:
            start_response('200 OK', headers)
            return ['Sorry, username {} is taken'.format(un).encode()]
        else:
            connection.execute('INSERT INTO login VALUES (?, ?)', [un, pw])
            connection.commit()
            start_response('200 OK', headers)
            return ['Username {} was successfully registered'.format(un).encode()]

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM login WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            start_response('200 OK', headers)
            return ['User {} has successfully logged in'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password'.encode()]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]

httpd = wsgiref.simple_server.make_server('', 8000, login_app)
httpd.serve_forever()