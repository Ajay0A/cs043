import wsgiref.simple_server
import http.cookies


def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8'),
               ('Set-Cookie', 'Name=Ajay'),
               ('Set-Cookie', 'Number=7'),
               ('Set-Cookie', 'Color=Green')]

    if 'HTTP_COOKIE' in environ:
        start_response('200 OK', headers)
        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        result = ''
        for key in cookies:
            result += (key + ': ' + cookies[key].value + '\n')
        return [result.encode()]
    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)

print('Serving on port 8000...')

httpd.serve_forever()