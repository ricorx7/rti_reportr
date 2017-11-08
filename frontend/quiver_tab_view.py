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
        self.tabWidget = QtWidgets.QTabWidget(Quiver_Tab)
        self.tabWidget.setGeometry(QtCore.QRect(0, 70, 701, 691))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.redrawButton = QtWidgets.QPushButton(Quiver_Tab)
        self.redrawButton.setGeometry(QtCore.QRect(590, 40, 113, 32))
        self.redrawButton.setObjectName("redrawButton")

        self.retranslateUi(Quiver_Tab)
        QtCore.QMetaObject.connectSlotsByName(Quiver_Tab)

    def retranslateUi(self, Quiver_Tab):
        _translate = QtCore.QCoreApplication.translate
        Quiver_Tab.setWindowTitle(_translate("Quiver_Tab", "MainWindow"))
        self.projectLabel.setText(_translate("Quiver_Tab", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Quiver_Tab", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Quiver_Tab", "Tab 2"))
        self.redrawButton.setText(_translate("Quiver_Tab", "Redraw"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Quiver_Tab = QtWidgets.QWidget()
    ui = Ui_Quiver_Tab()
    ui.setupUi(Quiver_Tab)
    Quiver_Tab.show()
    sys.exit(app.exec_())

