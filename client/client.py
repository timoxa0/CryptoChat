from asyncconsole import AsyncConsole
from cryptmgr import Cryptor
import threading
import argparse
import socket
import signal
import curses
import sys

parser = argparse.ArgumentParser(description='Timoxa0`s secure chat client')
parser.add_argument(
    'client_id',
    type=str,
    help='client ID in chat'
)
parser.add_argument(
    'target_id',
    type=str,
    help='target ID in chat'
)
parser.add_argument(
    'host',
    type=str,
    help='IP address of chat server'
)
parser.add_argument(
    '-p',
    '--port',
    default=45678,
    metavar='PORT',
    type=int,
    help='port of chat server'
)
parser.add_argument(
    '-k',
    '--key-file',
    default='key.aes',
    metavar='PATH',
    type=str,
    help='path to AES key-file'
)

args = parser.parse_args()

client_name = args.client_id.encode()
target_name = args.target_id.encode()


def sigint_handler(sig, frame):
    conn.send(b'close\r')
    conn.close()
    print('Socket closed. Exiting...')
    sys.exit(0)


cryptor = Cryptor(args.key_file)
signal.signal(signal.SIGINT, sigint_handler)
conn = socket.socket()
conn.connect((args.host, args.port))
conn.send(client_name)


class MyThread(threading.Thread):
    stop = False
    console = None

    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):

        while not self.stop:
            buff = 4096  # 4 KiB
            data = b''
            try:
                while not self.stop:
                    part = conn.recv(buff)
                    data += part
                    if len(part) < buff and data:
                        # either 0 or end of data
                        break
            except OSError:
                pass
            cmds = data.split(b'\r')
            for cmdline in cmds:
                if cmdline != b'':
                    self.console.addline(f'[FROM] -> {cryptor.decrypt(cmdline).decode("utf-8")}')


def main(stdscr):
    console = AsyncConsole(stdscr)
    t = MyThread()
    t.console = console
    t.start()
    try:
        while console.readline():
            if console.input_string in ['!quit', '!q', '!wq']:
                conn.send(b'close\r')
                conn.close()
                break
            msg = console.input_string
            console.addline(f'[TO] <- {msg}')
            conn.send(b'send' + b' ' + target_name + b' ' + cryptor.encrypt(msg.encode('utf-8')) + b'\r')
    finally:

        print('Socket closed. Exiting...')
        t.stop = True
        sys.exit(0)


if __name__ == '__main__':
    curses.wrapper(main)

