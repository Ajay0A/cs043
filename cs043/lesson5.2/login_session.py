import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies

connection = sqlite3.connect('login.db')
cursor = connection.cursor()


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
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            return ['Username {} was successfully registered'.format(un).encode()]

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM login WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            return ['User {} has successfully logged in'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password'.encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        return ['Logged out'.encode()]

    elif path == '/account':
        start_response('200 OK', headers)
        if 'HTTP_COOKIE' not in environ:
            return ['Not logged in'.encode()]
        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'session' not in cookies:
            return ['Not logged in'.encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute('SELECT * FROM login WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            return ['{} is logged in'.format(un).encode()]
        else:
            return ['Not logged in'.encode()]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]

httpd = wsgiref.simple_server.make_server('', 8000, login_app)
httpd.serve_forever()