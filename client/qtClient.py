import os.path
import socket
import sys

from PySide6 import QtGui
from PySide6.QtCore import QDir, QThread, QObject, Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QInputDialog, QLineEdit

from QtGui import Ui_MainWindow
from cryptmgr import Cryptor
from favctl import Favorites


class Sig(QObject):
    update = Signal(str)


class readThread(QThread):
    stop = False
    cryptor = None

    def __init__(self, parent=None, conn=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.signal = Sig()
        self.conn = conn

    def run(self):

        while not self.stop:
            buff = 4096  # 4 KiB
            data = b''
            try:
                while not self.stop:
                    part = self.conn.recv(buff)
                    data += part
                    if len(part) < buff and data:
                        # either 0 or end of data
                        break
            except OSError:
                pass
            cmds = data.split(b'\r')
            for cmdline in cmds:
                if cmdline != b'':
                    self.signal.update.emit(f'[FROM] -> {self.cryptor.decrypt(cmdline).decode("utf-8")}')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        # UI Setup
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Shortcuts
        self.ui.sendBtn.clicked.connect(self.send)
        self.sendShortcut = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+Return'), self)
        self.sendShortcut.activated.connect(self.send)

        # Chat menu
        self.ui.actionQuit.triggered.connect(lambda: self.quit_handler(quit=True))
        self.ui.actionOpen_Key_File.triggered.connect(self.select_keyfile)
        self.ui.actionGenerate_Key_File.triggered.connect(self.create_keyfile)
        self.ui.actionSet_ID.triggered.connect(self.set_id)
        self.ui.actionSet_Target_ID.triggered.connect(self.set_target_id)
        self.ui.actionSet_Server.triggered.connect(self.set_server)
        self.ui.actionConnect.triggered.connect(self.connect_handler)
        self.ui.statusbar.setText('Status: Disconnected')

        # Favorites menu
        self.ui.actionAdd.triggered.connect(self.add_handler)
        self.ui.actionRemove.triggered.connect(self.remove_handler)
        self.ui.actionSelect.triggered.connect(self.select_handler)

        # Vars
        self.cryptor = None
        self.id = None
        self.server = None
        self.connected = False
        self.socket = None
        self.t = None
        self.target_id = None
        self.keyfile = None

        # Favorites
        self.favorites = Favorites('favorites.db')

    @staticmethod
    def spawn_msgbox(msg):
        msgbox = QMessageBox()
        msgbox.setWindowTitle('CChat')
        msgbox.setText(msg)
        msgbox.exec()

    # NotImplemented handler
    def not_implemented_handler(self):
        self.spawn_msgbox('Not Implemented!')

    # Close button capture
    def closeEvent(self, event):
        self.quit_handler(quit=False)
        event.accept()

    # Send message logic
    def send(self):
        text = self.ui.msgEdit.toPlainText()
        if text.replace('\n', '') != '' and self.connected:
            self.socket.send(
                b'send' + b' ' + self.target_id.encode() + b' ' + self.cryptor.encrypt(text.encode('utf-8')) + b'\r')
            nl = '\n'
            self.ui.textPane.setText(f'{self.ui.textPane.toPlainText()}{nl}[TO] <- {text}')
            self.ui.textPane.verticalScrollBar().setValue(self.ui.textPane.verticalScrollBar().maximum())
        self.ui.msgEdit.setText('')

    # Select Key-File
    def select_keyfile(self):
        dialog = QFileDialog(self, 'Open Key-File', '.', 'Key-Files (*.aes)')
        filename = dialog.getOpenFileName(self)[0]
        if filename != '':
            self.keyfile = filename
            self.cryptor = Cryptor(filename)
            self.spawn_msgbox('Key-File selected!')

    # Create and Select Key-File
    def create_keyfile(self):
        dialog = QFileDialog(self, 'Save Key-File', '.', 'Key-Files (*.aes)')
        filename = dialog.getSaveFileName(self)[0]
        if filename != '':
            self.cryptor = Cryptor(filename)
            self.spawn_msgbox('Key-File generated!')

    # Set User-ID
    def set_id(self):
        text, ok = QInputDialog.getText(
            self,
            'Set User-ID',
            'User-ID',
            QLineEdit.Normal,
            QDir.home().dirName()
        )
        if ok and text:
            self.id = text

    # Set Traget-ID
    def set_target_id(self):
        text, ok = QInputDialog.getText(
            self,
            'Set Target-ID',
            'Target-ID',
            QLineEdit.Normal,
            'target'
        )
        if ok and text:
            self.target_id = text

    # Set server Ip:Port
    def set_server(self):
        text, ok = QInputDialog.getText(
            self,
            'Set Server',
            'Server Ip:Port',
            QLineEdit.Normal,
            'localhost:1234'
        )
        if ok and text:
            self.server = list(text.split(':'))

    # Accept massage from RecvThread
    @Slot(str)
    def print_msg(self, msg):
        nl = '\n'
        self.ui.textPane.setText(f'{self.ui.textPane.toPlainText()}{nl}{msg}')
        self.ui.textPane.verticalScrollBar().setValue(self.ui.textPane.verticalScrollBar().maximum())

    # Server-Client logic
    def connect_handler(self):
        if self.connected:
            self.t.stop = True
            self.socket.send(b'close\r')
            self.socket.close()
            self.ui.statusbar.setText(
                f'Status: Disconnected / {self.id} / {self.target_id} / {self.server[0]}:{self.server[1]}'
            )
            self.connected = False
        else:
            if self.id and self.server and self.target_id and self.cryptor:
                try:
                    self.socket = socket.socket()
                    self.socket.connect((self.server[0], int(self.server[1])))
                    self.socket.send(self.id.encode())
                    self.t = readThread(conn=self.socket)
                    self.t.stop = False
                    self.t.cryptor = self.cryptor
                    self.t.signal.update.connect(self.print_msg)
                    self.t.start()
                    self.ui.statusbar.setText(
                        f'Status: Connected / {self.id} / {self.target_id} / {self.server[0]}:{self.server[1]}')
                    self.connected = True
                except ConnectionRefusedError:
                    self.spawn_msgbox('Error: Connection Refused')

            else:
                self.spawn_msgbox('Please set ID, Target-ID, Server and Key-File')

    # Quit logic
    def quit_handler(self, quit=True):
        if self.connected:
            self.connect_handler()
        if quit:
            sys.exit(0)

    def add_handler(self):
        if self.id and self.server and self.target_id and self.keyfile:
            self.favorites.add(self.id, self.target_id, self.server[0], self.server[1], self.keyfile)
            self.spawn_msgbox('Bookmark added')
        else:
            self.spawn_msgbox('Please set ID, Target-ID, Server and Key-File')

    def select_favorite(self):
        items = {}
        for i in self.favorites.get():
            tmp = [str(j) for j in i]
            tmp[-1] = os.path.relpath(tmp[-1], '.')
            items['|'.join(tmp[1:])] = tmp[0]
        item, ok = QInputDialog().getItem(self, "Favorites", "Favorite:",
                                          list(items) if items != {} else ['No bookmark found'], 0, False)
        if ok and item and item != 'No bookmark found':
            return items[item]

    def select_handler(self):
        item_id = self.select_favorite()
        if item_id:
            try:
                item = self.favorites.get(string_id=item_id)[0][1:]
                print(item)
                self.id = item[0]
                self.target_id = item[1]
                self.server = []
                self.server.append(item[2])
                self.server.append(item[3])
                self.cryptor = Cryptor(item[4])
                self.spawn_msgbox('Bookmark loaded')
            except IndexError:
                self.server = None
                self.spawn_msgbox('Internal Error')

    def remove_handler(self):
        item_id = self.select_favorite()
        if item_id:
            self.favorites.remove(string_id=item_id)
            self.spawn_msgbox('Bookmark removed')


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
