# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'overall_tab_view.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Overall_Tab(object):
    def setupUi(self, Overall_Tab):
        Overall_Tab.setObjectName("Overall_Tab")
        Overall_Tab.resize(766, 826)
        self.projectLabel = QtWidgets.QLabel(Overall_Tab)
        self.projectLabel.setGeometry(QtCore.QRect(110, 90, 301, 31))
        self.projectLabel.setObjectName("projectLabel")
        self.summaryTextEdit = QtWidgets.QTextEdit(Overall_Tab)
        self.summaryTextEdit.setGeometry(QtCore.QRect(10, 140, 741, 451))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.summaryTextEdit.setFont(font)
        self.summaryTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.summaryTextEdit.setReadOnly(True)
        self.summaryTextEdit.setTabStopWidth(86)
        self.summaryTextEdit.setObjectName("summaryTextEdit")

        self.retranslateUi(Overall_Tab)
        QtCore.QMetaObject.connectSlotsByName(Overall_Tab)

    def retranslateUi(self, Overall_Tab):
        _translate = QtCore.QCoreApplication.translate
        Overall_Tab.setWindowTitle(_translate("Overall_Tab", "MainWindow"))
        self.projectLabel.setText(_translate("Overall_Tab", "TextLabel"))
        self.summaryTextEdit.setPlaceholderText(_translate("Overall_Tab", "Loading..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Overall_Tab = QtWidgets.QWidget()
    ui = Ui_Overall_Tab()
    ui.setupUi(Overall_Tab)
    Overall_Tab.show()
    sys.exit(app.exec_())

