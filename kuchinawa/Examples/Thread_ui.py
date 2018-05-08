# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Yuki\Dropbox\python\my_module_root\kuchinawa\kuchinawa\Examples\Thread.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(603, 648)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(40, 40, 481, 141))
        self.groupBox.setObjectName("groupBox")
        self.lcd1 = QtWidgets.QLCDNumber(self.groupBox)
        self.lcd1.setGeometry(QtCore.QRect(10, 40, 241, 61))
        self.lcd1.setDigitCount(7)
        self.lcd1.setObjectName("lcd1")
        self.button1 = QtWidgets.QPushButton(self.groupBox)
        self.button1.setGeometry(QtCore.QRect(270, 20, 93, 28))
        self.button1.setObjectName("button1")
        self.bar1 = QtWidgets.QProgressBar(self.groupBox)
        self.bar1.setGeometry(QtCore.QRect(300, 90, 118, 23))
        self.bar1.setProperty("value", 0)
        self.bar1.setObjectName("bar1")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(40, 220, 481, 141))
        self.groupBox_2.setObjectName("groupBox_2")
        self.lcd2 = QtWidgets.QLCDNumber(self.groupBox_2)
        self.lcd2.setGeometry(QtCore.QRect(10, 40, 241, 61))
        self.lcd2.setDigitCount(7)
        self.lcd2.setObjectName("lcd2")
        self.button2 = QtWidgets.QPushButton(self.groupBox_2)
        self.button2.setGeometry(QtCore.QRect(270, 20, 93, 28))
        self.button2.setObjectName("button2")
        self.bar2 = QtWidgets.QProgressBar(self.groupBox_2)
        self.bar2.setGeometry(QtCore.QRect(300, 90, 118, 23))
        self.bar2.setProperty("value", 0)
        self.bar2.setObjectName("bar2")
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setGeometry(QtCore.QRect(40, 410, 481, 141))
        self.groupBox_3.setObjectName("groupBox_3")
        self.lcd3 = QtWidgets.QLCDNumber(self.groupBox_3)
        self.lcd3.setGeometry(QtCore.QRect(10, 40, 241, 61))
        self.lcd3.setDigitCount(7)
        self.lcd3.setObjectName("lcd3")
        self.button3 = QtWidgets.QPushButton(self.groupBox_3)
        self.button3.setGeometry(QtCore.QRect(270, 20, 93, 28))
        self.button3.setObjectName("button3")
        self.bar3 = QtWidgets.QProgressBar(self.groupBox_3)
        self.bar3.setGeometry(QtCore.QRect(300, 90, 118, 23))
        self.bar3.setProperty("value", 0)
        self.bar3.setObjectName("bar3")
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.groupBox_2.raise_()
        self.groupBox_3.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Thread1"))
        self.button1.setText(_translate("Form", "terminate"))
        self.groupBox_2.setTitle(_translate("Form", "Thread2"))
        self.button2.setText(_translate("Form", "terminate"))
        self.groupBox_3.setTitle(_translate("Form", "Thread3"))
        self.button3.setText(_translate("Form", "terminate"))

