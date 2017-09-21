import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from frontend import mainwindow

# Include the RTI python library
import sys
sys.path.append('rti_python/')


'''
This file is created so that the main is started at the top level.
Then all imports from rti_python can then be included into the frontend
folder.
'''
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Mac")

    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainwindow.MainWindow()
    sys.exit(app.exec_())