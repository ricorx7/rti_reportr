# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'location_tab_view.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Location_Tab(object):
    def setupUi(self, Location_Tab):
        Location_Tab.setObjectName("Location_Tab")
        Location_Tab.resize(766, 826)
        self.projectLabel = QtWidgets.QLabel(Location_Tab)
        self.projectLabel.setGeometry(QtCore.QRect(10, 30, 301, 31))
        self.projectLabel.setObjectName("projectLabel")
        self.summaryTextEdit = QtWidgets.QTextEdit(Location_Tab)
        self.summaryTextEdit.setGeometry(QtCore.QRect(10, 70, 601, 451))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.summaryTextEdit.setFont(font)
        self.summaryTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.summaryTextEdit.setReadOnly(True)
        self.summaryTextEdit.setTabStopWidth(86)
        self.summaryTextEdit.setObjectName("summaryTextEdit")

        self.retranslateUi(Location_Tab)
        QtCore.QMetaObject.connectSlotsByName(Location_Tab)

    def retranslateUi(self, Location_Tab):
        _translate = QtCore.QCoreApplication.translate
        Location_Tab.setWindowTitle(_translate("Location_Tab", "MainWindow"))
        self.projectLabel.setText(_translate("Location_Tab", "TextLabel"))
        self.summaryTextEdit.setPlaceholderText(_translate("Location_Tab", "Loading..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Location_Tab = QtWidgets.QWidget()
    ui = Ui_Location_Tab()
    ui.setupUi(Location_Tab)
    Location_Tab.show()
    sys.exit(app.exec_())

