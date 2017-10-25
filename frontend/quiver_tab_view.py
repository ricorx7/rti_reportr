# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quiver_tab_view.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Quiver_Tab(object):
    def setupUi(self, Quiver_Tab):
        Quiver_Tab.setObjectName("Quiver_Tab")
        Quiver_Tab.resize(766, 826)
        self.projectLabel = QtWidgets.QLabel(Quiver_Tab)
        self.projectLabel.setGeometry(QtCore.QRect(10, 30, 301, 31))
        self.projectLabel.setObjectName("projectLabel")
        self.summaryTextEdit = QtWidgets.QTextEdit(Quiver_Tab)
        self.summaryTextEdit.setGeometry(QtCore.QRect(0, 70, 761, 131))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.summaryTextEdit.setFont(font)
        self.summaryTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.summaryTextEdit.setReadOnly(True)
        self.summaryTextEdit.setTabStopWidth(86)
        self.summaryTextEdit.setObjectName("summaryTextEdit")
        self.htmlWidget = QtWidgets.QWidget(Quiver_Tab)
        self.htmlWidget.setGeometry(QtCore.QRect(0, 218, 760, 600))
        self.htmlWidget.setObjectName("htmlWidget")

        self.retranslateUi(Quiver_Tab)
        QtCore.QMetaObject.connectSlotsByName(Quiver_Tab)

    def retranslateUi(self, Quiver_Tab):
        _translate = QtCore.QCoreApplication.translate
        Quiver_Tab.setWindowTitle(_translate("Quiver_Tab", "MainWindow"))
        self.projectLabel.setText(_translate("Quiver_Tab", "TextLabel"))
        self.summaryTextEdit.setPlaceholderText(_translate("Quiver_Tab", "Loading..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Quiver_Tab = QtWidgets.QWidget()
    ui = Ui_Quiver_Tab()
    ui.setupUi(Quiver_Tab)
    Quiver_Tab.show()
    sys.exit(app.exec_())

