# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(351, 331)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(30, 20, 291, 231))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 30, 241, 131))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.config_graph_clear = QtWidgets.QComboBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.config_graph_clear.sizePolicy().hasHeightForWidth())
        self.config_graph_clear.setSizePolicy(sizePolicy)
        self.config_graph_clear.setEditable(False)
        self.config_graph_clear.setMaxVisibleItems(2)
        self.config_graph_clear.setObjectName("config_graph_clear")
        self.config_graph_clear.addItem("")
        self.config_graph_clear.addItem("")
        self.gridLayout.addWidget(self.config_graph_clear, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.config_graph_rate = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.config_graph_rate.setMinimum(100)
        self.config_graph_rate.setMaximum(10000)
        self.config_graph_rate.setSingleStep(100)
        self.config_graph_rate.setObjectName("config_graph_rate")
        self.gridLayout.addWidget(self.config_graph_rate, 1, 1, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.pushButton_ok = QtWidgets.QPushButton(Form)
        self.pushButton_ok.setGeometry(QtCore.QRect(120, 280, 81, 28))
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.pushButton_cancel = QtWidgets.QPushButton(Form)
        self.pushButton_cancel.setGeometry(QtCore.QRect(220, 280, 93, 28))
        self.pushButton_cancel.setObjectName("pushButton_cancel")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        self.config_graph_clear.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "clear when restarting"))
        self.config_graph_clear.setCurrentText(_translate("Form", "True"))
        self.config_graph_clear.setItemText(0, _translate("Form", "True"))
        self.config_graph_clear.setItemText(1, _translate("Form", "False"))
        self.label_2.setText(_translate("Form", "update interval (/ms)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Graph"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Blank"))
        self.pushButton_ok.setText(_translate("Form", "Apply"))
        self.pushButton_cancel.setText(_translate("Form", "Cancel"))

