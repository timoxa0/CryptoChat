import socket


def recvall(connection):
    buffer = 4096  # 4 KiB
    data = b''
    while True:
        part = connection.recv(buffer)
        data += part
        if len(part) < buffer and data:
            # either 0 or end of data
            break
    return data.split(b'\r')


conn = socket.socket()
conn.connect(('127.0.0.1', 45651))

conn.send(b'test2')
print(recvall(conn)[0].decode())
conn.send(b'send test test\r')
conn.send(b'send test test\r')
conn.send(b'close\r')
