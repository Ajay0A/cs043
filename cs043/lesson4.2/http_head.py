def http_head(host, page):
    import socket
    sock = socket.create_connection((host, 80))
    sock.sendall(('HEAD ' + page + ' HTTP/1.1\r\nHost: ' + host + '\r\n\r\n').encode())
    print(sock.recv(1000).decode())
    sock.close()

#http_head('www.google.com', '/')
http_head('50.87.178.13', '/CScourses/03b2_minimal-meta.html')