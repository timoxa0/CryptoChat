# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'client.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(618, 404)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionConnect = QAction(MainWindow)
        self.actionConnect.setObjectName(u"actionConnect")
        self.actionSet_ID = QAction(MainWindow)
        self.actionSet_ID.setObjectName(u"actionSet_ID")
        self.actionOpen_Key_File = QAction(MainWindow)
        self.actionOpen_Key_File.setObjectName(u"actionOpen_Key_File")
        self.actionSet_Server = QAction(MainWindow)
        self.actionSet_Server.setObjectName(u"actionSet_Server")
        self.actionGenerate_Key_File = QAction(MainWindow)
        self.actionGenerate_Key_File.setObjectName(u"actionGenerate_Key_File")
        self.actionSet_Target_ID = QAction(MainWindow)
        self.actionSet_Target_ID.setObjectName(u"actionSet_Target_ID")
        self.actionAdd = QAction(MainWindow)
        self.actionAdd.setObjectName(u"actionAdd")
        self.actionRemove = QAction(MainWindow)
        self.actionRemove.setObjectName(u"actionRemove")
        self.actionSelect = QAction(MainWindow)
        self.actionSelect.setObjectName(u"actionSelect")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textPane = QTextEdit(self.centralwidget)
        self.textPane.setObjectName(u"textPane")
        self.textPane.setMinimumSize(QSize(600, 100))
        self.textPane.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.textPane)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.msgEdit = QTextEdit(self.centralwidget)
        self.msgEdit.setObjectName(u"msgEdit")
        self.msgEdit.setMaximumSize(QSize(16777215, 50))
        self.msgEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.horizontalLayout.addWidget(self.msgEdit)

        self.sendBtn = QPushButton(self.centralwidget)
        self.sendBtn.setObjectName(u"sendBtn")
        self.sendBtn.setMinimumSize(QSize(0, 50))
        self.sendBtn.setStyleSheet(u"QPushButton {\n"
"	\n"
"}")

        self.horizontalLayout.addWidget(self.sendBtn)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.statusbar = QLabel(self.centralwidget)
        self.statusbar.setObjectName(u"statusbar")

        self.verticalLayout_2.addWidget(self.statusbar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 618, 24))
        self.menuChat = QMenu(self.menuBar)
        self.menuChat.setObjectName(u"menuChat")
        self.menuFavorites = QMenu(self.menuBar)
        self.menuFavorites.setObjectName(u"menuFavorites")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuChat.menuAction())
        self.menuBar.addAction(self.menuFavorites.menuAction())
        self.menuChat.addAction(self.actionSet_ID)
        self.menuChat.addAction(self.actionSet_Target_ID)
        self.menuChat.addAction(self.actionSet_Server)
        self.menuChat.addAction(self.actionOpen_Key_File)
        self.menuChat.addAction(self.actionGenerate_Key_File)
        self.menuChat.addSeparator()
        self.menuChat.addAction(self.actionConnect)
        self.menuChat.addSeparator()
        self.menuChat.addAction(self.actionQuit)
        self.menuFavorites.addAction(self.actionAdd)
        self.menuFavorites.addAction(self.actionRemove)
        self.menuFavorites.addAction(self.actionSelect)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CChat", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionConnect.setText(QCoreApplication.translate("MainWindow", u"Connect/Disconnect", None))
        self.actionSet_ID.setText(QCoreApplication.translate("MainWindow", u"Set ID", None))
        self.actionOpen_Key_File.setText(QCoreApplication.translate("MainWindow", u"Open Key-File", None))
        self.actionSet_Server.setText(QCoreApplication.translate("MainWindow", u"Set Server", None))
        self.actionGenerate_Key_File.setText(QCoreApplication.translate("MainWindow", u"Generate Key-File", None))
        self.actionSet_Target_ID.setText(QCoreApplication.translate("MainWindow", u"Set Target-ID", None))
        self.actionAdd.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.actionRemove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.actionSelect.setText(QCoreApplication.translate("MainWindow", u"Use", None))
        self.sendBtn.setText(QCoreApplication.translate("MainWindow", u"Send", None))
        self.statusbar.setText(QCoreApplication.translate("MainWindow", u"Status: <Not Set>", None))
        self.menuChat.setTitle(QCoreApplication.translate("MainWindow", u"Chat", None))
        self.menuFavorites.setTitle(QCoreApplication.translate("MainWindow", u"Bookmarks", None))
    # retranslateUi

