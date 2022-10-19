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

conn.send(b'test')
while True:
    cmds = recvall(conn)
    print(cmds)

    for cmdline in cmds:
        print('\t', cmdline, sep='')
    if input() == 'q':
        break
conn.send(b'close\r')
