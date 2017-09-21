# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportr_view.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RoweTechReportR(object):
    def setupUi(self, RoweTechReportR):
        RoweTechReportR.setObjectName("RoweTechReportR")
        RoweTechReportR.resize(1045, 874)
        self.centralWidget = QtWidgets.QWidget(RoweTechReportR)
        self.centralWidget.setObjectName("centralWidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 291, 221))
        self.groupBox.setObjectName("groupBox")
        self.selectFileButton = QtWidgets.QPushButton(self.groupBox)
        self.selectFileButton.setGeometry(QtCore.QRect(20, 30, 271, 32))
        self.selectFileButton.setObjectName("selectFileButton")
        self.selectedFileListView = QtWidgets.QListWidget(self.groupBox)
        self.selectedFileListView.setGeometry(QtCore.QRect(30, 60, 256, 111))
        self.selectedFileListView.setObjectName("selectedFileListView")
        self.loadButton = QtWidgets.QPushButton(self.groupBox)
        self.loadButton.setGeometry(QtCore.QRect(180, 180, 113, 32))
        self.loadButton.setObjectName("loadButton")
        self.tabSubsystem = QtWidgets.QTabWidget(self.centralWidget)
        self.tabSubsystem.setEnabled(True)
        self.tabSubsystem.setGeometry(QtCore.QRect(320, 30, 671, 811))
        self.tabSubsystem.setObjectName("tabSubsystem")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabSubsystem.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabSubsystem.addTab(self.tab_4, "")
        RoweTechReportR.setCentralWidget(self.centralWidget)

        self.retranslateUi(RoweTechReportR)
        self.tabSubsystem.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(RoweTechReportR)

    def retranslateUi(self, RoweTechReportR):
        _translate = QtCore.QCoreApplication.translate
        RoweTechReportR.setWindowTitle(_translate("RoweTechReportR", "MainWindow"))
        self.groupBox.setTitle(_translate("RoweTechReportR", "File"))
        self.selectFileButton.setText(_translate("RoweTechReportR", "Select File"))
        self.loadButton.setText(_translate("RoweTechReportR", "LOAD"))
        self.tabSubsystem.setTabText(self.tabSubsystem.indexOf(self.tab_3), _translate("RoweTechReportR", "Tab 1"))
        self.tabSubsystem.setTabText(self.tabSubsystem.indexOf(self.tab_4), _translate("RoweTechReportR", "Tab 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RoweTechReportR = QtWidgets.QMainWindow()
    ui = Ui_RoweTechReportR()
    ui.setupUi(RoweTechReportR)
    RoweTechReportR.show()
    sys.exit(app.exec_())

