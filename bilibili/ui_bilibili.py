# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bilibili.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTextBrowser, QVBoxLayout, QWidget)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.resize(1413, 785)
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.LABEL_URL = QLabel(self.centralwidget)
        self.LABEL_URL.setObjectName(u"LABEL_URL")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LABEL_URL.sizePolicy().hasHeightForWidth())
        self.LABEL_URL.setSizePolicy(sizePolicy)
        self.LABEL_URL.setMinimumSize(QSize(100, 0))
        self.LABEL_URL.setMaximumSize(QSize(100, 16777215))
        font = QFont()
        font.setPointSize(12)
        self.LABEL_URL.setFont(font)
        self.LABEL_URL.setLayoutDirection(Qt.LeftToRight)
        self.LABEL_URL.setAutoFillBackground(False)
        self.LABEL_URL.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.LABEL_URL)

        self.LABEL_Cookies = QLabel(self.centralwidget)
        self.LABEL_Cookies.setObjectName(u"LABEL_Cookies")
        sizePolicy.setHeightForWidth(self.LABEL_Cookies.sizePolicy().hasHeightForWidth())
        self.LABEL_Cookies.setSizePolicy(sizePolicy)
        self.LABEL_Cookies.setMinimumSize(QSize(100, 0))
        self.LABEL_Cookies.setMaximumSize(QSize(100, 16777215))
        self.LABEL_Cookies.setFont(font)
        self.LABEL_Cookies.setLayoutDirection(Qt.LeftToRight)
        self.LABEL_Cookies.setAutoFillBackground(False)
        self.LABEL_Cookies.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.LABEL_Cookies)

        self.EDIT_Cookies = QPlainTextEdit(self.centralwidget)
        self.EDIT_Cookies.setObjectName(u"EDIT_Cookies")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.EDIT_Cookies)

        self.LABEL_Comment = QLabel(self.centralwidget)
        self.LABEL_Comment.setObjectName(u"LABEL_Comment")
        sizePolicy.setHeightForWidth(self.LABEL_Comment.sizePolicy().hasHeightForWidth())
        self.LABEL_Comment.setSizePolicy(sizePolicy)
        self.LABEL_Comment.setMinimumSize(QSize(100, 0))
        self.LABEL_Comment.setMaximumSize(QSize(100, 16777215))
        self.LABEL_Comment.setFont(font)
        self.LABEL_Comment.setLayoutDirection(Qt.LeftToRight)
        self.LABEL_Comment.setAutoFillBackground(False)
        self.LABEL_Comment.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.LABEL_Comment)

        self.LABEL_Rpid = QLabel(self.centralwidget)
        self.LABEL_Rpid.setObjectName(u"LABEL_Rpid")
        sizePolicy.setHeightForWidth(self.LABEL_Rpid.sizePolicy().hasHeightForWidth())
        self.LABEL_Rpid.setSizePolicy(sizePolicy)
        self.LABEL_Rpid.setMinimumSize(QSize(100, 0))
        self.LABEL_Rpid.setMaximumSize(QSize(100, 16777215))
        self.LABEL_Rpid.setFont(font)
        self.LABEL_Rpid.setLayoutDirection(Qt.LeftToRight)
        self.LABEL_Rpid.setAutoFillBackground(False)
        self.LABEL_Rpid.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.LABEL_Rpid)

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.textBrowser)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.BTN_Send = QPushButton(self.centralwidget)
        self.BTN_Send.setObjectName(u"BTN_Send")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.BTN_Send.sizePolicy().hasHeightForWidth())
        self.BTN_Send.setSizePolicy(sizePolicy1)
        self.BTN_Send.setMinimumSize(QSize(200, 50))
        self.BTN_Send.setMaximumSize(QSize(200, 50))
        self.BTN_Send.setFont(font)

        self.horizontalLayout_3.addWidget(self.BTN_Send)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.EDIT_URL = QPlainTextEdit(self.centralwidget)
        self.EDIT_URL.setObjectName(u"EDIT_URL")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.EDIT_URL)

        self.EDIT_Comment = QPlainTextEdit(self.centralwidget)
        self.EDIT_Comment.setObjectName(u"EDIT_Comment")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.EDIT_Comment)


        self.verticalLayout.addLayout(self.formLayout)

        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)

        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QCoreApplication.translate("mainWindow", u"Bilibili\u8bc4\u8bba\u5de5\u5177", None))
        self.LABEL_URL.setText(QCoreApplication.translate("mainWindow", u"URL\uff1a", None))
        self.LABEL_Cookies.setText(QCoreApplication.translate("mainWindow", u"Cookies\uff1a", None))
        self.LABEL_Comment.setText(QCoreApplication.translate("mainWindow", u"\u8bc4\u8bba\u5185\u5bb9\uff1a", None))
        self.LABEL_Rpid.setText(QCoreApplication.translate("mainWindow", u"\u8fd4\u56de\u7ed3\u679c\uff1a", None))
        self.BTN_Send.setText(QCoreApplication.translate("mainWindow", u"\u53d1\u9001", None))
    # retranslateUi

