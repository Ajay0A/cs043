import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies

connection = sqlite3.connect('login.db')
cursor = connection.cursor()

def login_app(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    param = urllib.parse.parse_qs(environ['QUERY_STRING'])
    path = environ['PATH_INFO']
    un = param['username'][0] if 'username' in param else True
    pw = param['password'][0] if 'password' in param else True

    if path == '/register' and un and pw:
        user = cursor.execute('SELECT * FROM login WHERE username = ?', [un]).fetchall()

        if user:
            start_response('200 OK', headers)
            return ['Sorry, username {} is taken'.format(un).encode()]
        else:
            page = '''<!DOCTYPE html>
            <form action='/register'>
                <h1>Register</h1>
                Username <input type="text" name="username">
                <br>
                Password <input type="password" name="password"><br>
                <br>
                <input type="submit" value="Register"><br>
                <hr>
            </form>'''

            connection.execute('INSERT INTO login VALUES (?, ?)', [un, pw])
            connection.commit()
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            if un == True:
                return[page.encode()]
            else:
                return [page.encode(), 'Username {} was successfully registered. <br><br><a href="/account">Account</a>'.format(un).encode()]

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM login WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            page = '''<!DOCTYPE html>
            <form action="/login">
            <h1>Login</h1>
            Username <input type="text" name="username"><br>
            Password <input type="password" name="password"><br>
            <input type="submit" value="Log in">
            </form>'''
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            if un == True:
                return[page.encode()]
            else:
                return [page.encode(), 'User {} has successfully logged in.<br><br><a href="/account">Account</a>'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password'.encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        return ['Logged out. <a href="/">Login</a>'.encode()]

    elif path == '/account':
        start_response('200 OK', headers)

        if 'HTTP_COOKIE' not in environ:
            return ['Not logged in.<br><br> <a href="/login">Login</a>'.encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'session' not in cookies:
            return ['Not logged in.<br><br> <a href="/login">Login</a>'.encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute('SELECT * FROM login WHERE username = ? AND password = ?', [un, pw]).fetchall()

        if user:
            return ['{} is logged in.<br><br> <a href="/logout">Logout</a>'.format(un).encode()]

        else:
            return ['Not logged in.<br><br> <a href="/login">Login</a>'.encode()]

    elif path == '/':
        page = '''<!DOCTYPE html>
        <a href="/login">Login</a><br><br>
        <a href="/register">Register</a>
        '''
        return [page.encode()]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, login_app)
httpd.serve_forever()
