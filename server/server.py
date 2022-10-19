import argparse
import asyncio
import socket
import sys

parser = argparse.ArgumentParser(description='Timoxa0`s secure chat server')
parser.add_argument(
    '--host',
    default='0.0.0.0',
    dest='host',
    type=str,
    help='HOST'
)
parser.add_argument(
    '--port',
    default=45678,
    metavar='port',
    type=int,
    help='PORT'
)
args = parser.parse_args()

clients = {}


async def handle_client(client):
    global clients
    loop = asyncio.get_event_loop()
    buffer = 4096  # 4 KiB
    data = b''
    while True:
        part = (await loop.sock_recv(client, buffer))
        data += part
        if len(part) < buffer and data:
            # either 0 or end of data
            break
    c_id = data.decode()
    if c_id in clients:
        print('Fake client connected. Closing fake connection')
        client.close()
    else:
        clients[c_id] = client
        print(f'Client {c_id} connected!')
        working = True
        is_loop = True
        while is_loop:
            data = b''
            while working:
                part = (await loop.sock_recv(client, buffer))
                data += part
                if len(part) < buffer and data:
                    # either 0 or end of data
                    break
            cmds = data.split(b'\r')
            for cmdline in cmds:
                if cmdline != b'':
                    cmd = cmdline.split()
                    print(cmd)
                    if cmd[0].decode() == 'send':
                        try:
                            await loop.sock_sendall(clients[cmd[1].decode()], b''.join(cmd[2:]) + b'\r')
                        except OSError as e:
                            print(f'An error occurred: {e}')
                        except KeyError as e:
                            print(f'Client {c_id} not found!')
                    if cmd[0].decode() == 'close':
                        is_loop = False
                        working = False
                        clients.pop(c_id)
                        client.close()
                        print(f'Client {c_id} disconnected!')
                        break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f'Server started at {args.host}:{args.port}')
server.bind((args.host, args.port))
server.listen(80)
server.setblocking(False)


async def run_server():
    loop = asyncio.get_event_loop()
    while True:
        client, _ = await loop.sock_accept(server)
        loop.create_task(handle_client(client))


if __name__ == '__main__':
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        for c_id in clients:
            clients[c_id].close()
        server.close()
        print('Sockets closed. Exiting...')
        sys.exit(0)

