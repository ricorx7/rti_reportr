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
        self.groupBox.setGeometry(QtCore.QRect(20, 250, 291, 221))
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
        self.tabReport = QtWidgets.QTabWidget(self.centralWidget)
        self.tabReport.setEnabled(True)
        self.tabReport.setGeometry(QtCore.QRect(320, 30, 711, 811))
        self.tabReport.setObjectName("tabReport")
        self.tabOverall = QtWidgets.QWidget()
        self.tabOverall.setObjectName("tabOverall")
        self.tabReport.addTab(self.tabOverall, "")
        self.tabAmplitude = QtWidgets.QWidget()
        self.tabAmplitude.setObjectName("tabAmplitude")
        self.tabReport.addTab(self.tabAmplitude, "")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 49, 291, 181))
        self.groupBox_2.setObjectName("groupBox_2")
        self.projectListWidget = QtWidgets.QListWidget(self.groupBox_2)
        self.projectListWidget.setGeometry(QtCore.QRect(20, 40, 256, 91))
        self.projectListWidget.setObjectName("projectListWidget")
        RoweTechReportR.setCentralWidget(self.centralWidget)

        self.retranslateUi(RoweTechReportR)
        self.tabReport.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(RoweTechReportR)

    def retranslateUi(self, RoweTechReportR):
        _translate = QtCore.QCoreApplication.translate
        RoweTechReportR.setWindowTitle(_translate("RoweTechReportR", "MainWindow"))
        self.groupBox.setTitle(_translate("RoweTechReportR", "File"))
        self.selectFileButton.setText(_translate("RoweTechReportR", "Select File"))
        self.loadButton.setText(_translate("RoweTechReportR", "LOAD"))
        self.tabReport.setTabText(self.tabReport.indexOf(self.tabOverall), _translate("RoweTechReportR", "Tab 1"))
        self.tabReport.setTabText(self.tabReport.indexOf(self.tabAmplitude), _translate("RoweTechReportR", "Tab 2"))
        self.groupBox_2.setTitle(_translate("RoweTechReportR", "Projects"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RoweTechReportR = QtWidgets.QMainWindow()
    ui = Ui_RoweTechReportR()
    ui.setupUi(RoweTechReportR)
    RoweTechReportR.show()
    sys.exit(app.exec_())

