import wsgiref.simple_server


def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    start_response('200 OK', headers)
    page = '''<!DOCTYPE html>
          <html>
          <head><title>Page Title</title></head>
          <body>Page Body</body>
          </html>'''

    return [page.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()
