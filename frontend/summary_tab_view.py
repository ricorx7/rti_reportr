# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'summary_tab_view.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Summary_Tab(object):
    def setupUi(self, Summary_Tab):
        Summary_Tab.setObjectName("Summary_Tab")
        Summary_Tab.resize(766, 826)
        self.projectLabel = QtWidgets.QLabel(Summary_Tab)
        self.projectLabel.setGeometry(QtCore.QRect(10, 30, 301, 31))
        self.projectLabel.setObjectName("projectLabel")
        self.summaryTextEdit = QtWidgets.QTextEdit(Summary_Tab)
        self.summaryTextEdit.setGeometry(QtCore.QRect(10, 70, 601, 451))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.summaryTextEdit.setFont(font)
        self.summaryTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.summaryTextEdit.setReadOnly(True)
        self.summaryTextEdit.setTabStopWidth(86)
        self.summaryTextEdit.setObjectName("summaryTextEdit")

        self.retranslateUi(Summary_Tab)
        QtCore.QMetaObject.connectSlotsByName(Summary_Tab)

    def retranslateUi(self, Summary_Tab):
        _translate = QtCore.QCoreApplication.translate
        Summary_Tab.setWindowTitle(_translate("Summary_Tab", "MainWindow"))
        self.projectLabel.setText(_translate("Summary_Tab", "TextLabel"))
        self.summaryTextEdit.setPlaceholderText(_translate("Summary_Tab", "Loading..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Summary_Tab = QtWidgets.QWidget()
    ui = Ui_Summary_Tab()
    ui.setupUi(Summary_Tab)
    Summary_Tab.show()
    sys.exit(app.exec_())

