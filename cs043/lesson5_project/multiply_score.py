import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies
import random

connection = sqlite3.connect('multiply.db')
stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='multiply'"
cursor = connection.cursor()
result = cursor.execute(stmt)
r = result.fetchall()
if r == []:
    exp = 'CREATE TABLE multiply (username,password, correct, wrong)'
    connection.execute(exp)


def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else True
    pw = params['password'][0] if 'password' in params else True
    correct = 0
    wrong = 0

    if path == '/register' and un and pw:
        user = cursor.execute('SELECT username FROM multiply WHERE username = ?', [un]).fetchall()
        if un is not True and user:
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

            connection.execute('INSERT INTO multiply VALUES (?, ?, ?, ?)', [un, pw, 0, 0])
            connection.commit()
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            if un is True:
                return[page.encode()]
            else:
                return [page.encode(), 'Username {} was successfully registered. <br><br><a href="/account">Account</a>'.format(un).encode()]

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT username, password FROM multiply WHERE username = ? AND password = ?', [un, pw]).fetchall()
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
            if un is True:
                return[page.encode()]
            else:
                return [page.encode(), 'User {} successfully logged in. <a href="/account">Account</a>'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password'.encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session={}:{}; expires=Thu, 01 Jan 1970 00:00:00 GMT'.format(un, pw)))
        headers.append(('Set-Cookie', 'score={}:{}; expires=Thu, 01 Jan 1970 00:00:00 GMT'.format(correct, wrong)))
        start_response('200 OK', headers)
        return ['Logged out. <a href="/">Login</a>'.encode()]

    elif path == '/account':
        start_response('200 OK', headers)

        if 'HTTP_COOKIE' not in environ:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'session' not in cookies:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute('SELECT username, password FROM multiply WHERE username = ? AND password = ?', [un, pw]).fetchall()

        if user:
            correct = 0
            wrong = 0

            if 'score' not in cookies:
                correct = cursor.execute('SELECT correct FROM multiply WHERE username = ? AND password = ?', [un, pw]).fetchall()
                correct = int(correct[0][0])
                wrong = cursor.execute('SELECT wrong FROM multiply WHERE username = ? AND password = ?', [un, pw]).fetchall()
                wrong = int(wrong[0][0])
                headers.append(('Set-Cookie', 'score={}:{}'.format(correct, wrong)))
                cookies.load('score={}:{}'.format(correct, wrong))

            else:
                cookies = http.cookies.SimpleCookie()
                cookies.load(environ['HTTP_COOKIE'])
            if 'HTTP_COOKIE' in environ:
                correct = int(cookies['score'].value.split(':')[0])
                wrong = int(cookies['score'].value.split(':')[1])

            page = '<!DOCTYPE html><html><head><title>Multiply with Score</title></head><body>'
            if 'factor1' in params and 'factor2' in params and 'answer' in params:
                f1 = int(params['factor1'][0])
                f2 = int(params['factor2'][0])
                answer = int(params['answer'][0])
                if f1*f2 == answer:
                    page += '<p style="background-color: lightgreen">Correct. {} x {} = {}'.format(f1, f2, answer)
                    correct += 1
                elif f1*f2 != answer:
                    page += '<p style="background-color: red">Wrong. {} x {} = {}'.format(f1, f2, answer)
                    wrong += 1

            elif 'reset' in params:
                correct = 0
                wrong = 0

            connection.execute('UPDATE multiply SET correct = ?, wrong = ? WHERE username = ?', [correct, wrong, un])
            connection.commit()

            headers.append(('Set-Cookie', 'score={}:{}'.format(correct, wrong)))

            f1 = random.randrange(10) + 1
            f2 = random.randrange(10) + 1

            page += '<h1>What is {} x {}</h1>'.format(f1, f2)
            r1 = random.randint(1, 100)
            r2 = random.randint(1, 100)
            r3 = random.randint(1, 100)
            a1 = f1*f2

            while r1 == a1 or r2 == a1 or r3 == a1:
                r1 = random.randint(1, 100)
                r2 = random.randint(1, 100)
                r3 = random.randint(1, 100)

            answer = [a1, r1, r2, r3]
            random.shuffle(answer)

            hyperlink = '<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">{}: {}</a><br>'

            page += hyperlink.format(un, pw, f1, f2, answer[0], 'A', answer[0])
            page += hyperlink.format(un, pw, f1, f2, answer[1], 'B', answer[1])
            page += hyperlink.format(un, pw, f1, f2, answer[2], 'C', answer[2])
            page += hyperlink.format(un, pw, f1, f2, answer[3], 'D', answer[3])

            page += '''<h2>Score</h2>
            Correct: {}<br>
            Wrong: {}<br>
            <a href="/account?reset=true">Reset</a>
            </body></html>'''.format(correct, wrong)

            return [page.encode()]
        else:
            return ['Not logged in. <a href="/">Login</a>'.encode()]

    elif path == '/':
        user = cursor.execute('SELECT username FROM multiply WHERE username = ?', [un]).fetchall()
        if un is not True and user:
            start_response('200 OK', headers)
            return ['Sorry, username {} is taken'.format(un).encode()]

        else:
            page = '''<!DOCTYPE html>
                <form action='/'>
                <h1>Register</h1>
                Username <input type="text" name="username"><br>
                Password <input type="password" name="password"><br>
                <br>
                <input type="submit" value="Register"><br>
                <hr>
                </form>
                <form>
                <h1>Login</h1>
                Username <input type="text" name="username2"><br>
                Password <input type="password" name="password2"><br>
                <br>
                <input type="submit" value="Log in">
                </form>'''
        if 'username' in params:
            connection.execute('INSERT INTO multiply VALUES (?, ?, ?, ?)', [un, pw, 0, 0])
            connection.commit()
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)

            if un is True:
                return [page.encode()]
            else:
                return [page.encode(),
                        'Username {} was successfully registered. <br><br><a href="/account">Account</a>'.format(un).encode()]
        elif 'username2' in params:
            un2 = params['username2'][0] if 'username2' in params else True
            pw2 = params['password2'][0] if 'password2' in params else True
            headers.append(('Set-Cookie', 'session={}:{}'.format(un2, pw2)))
            start_response('200 OK', headers)
            if un2 is True:
                return [page.encode()]
            else:
                return [page.encode(), 'User {} successfully logged in. <a href="/account">Account</a>'.format(un2).encode()]
        else:
            start_response('200 OK', headers)
            if un is True:
                return [page.encode()]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()
