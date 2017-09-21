import datetime
import os
import sys
from .reportr_view import Ui_RoweTechReportR
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .project_file import Project


import pandas as pd

class ReportrVM(Ui_RoweTechReportR):
    """

    """
    def __init__(self, parent):
        # Place the Import here because this import is also done within rti_python
        # which is causing it to overlap
        import rti_python.Codecs.AdcpCodec as codec

        Ui_RoweTechReportR.__init__(self)
        self.setupUi(parent)
        self.parent = parent

        # Create project file
        self.project_file = Project("projects.sqlite")

        # Create codec
        self.codec = codec.AdcpCodec()
        self.codec.EnsembleEvent += self.process_ensemble

        self.selectFileButton.clicked.connect(self.select_file_dialog)
        self.loadButton.clicked.connect(self.read_files)

    def select_file_dialog(self):
        # Clear the current selected items
        self.selectedFileListView.clear()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname, _ = QFileDialog.getOpenFileNames(None, "Select ADCP File", options=options)
        if fname:
            for file in fname:
                self.selectedFileListView.addItem(file)
                print(file)


    # Decode the ADCP data from the file path given
    def read_files(self):
        # Read in the data and decode it
        print("Reading files...")
        for x in range(self.selectedFileListView.count()):              # Load each file selected
            file = str(self.selectedFileListView.item(x).text())        # Get the file path from the list
            print("Loading: ", file)
            self.process_file(file)                                     # Process the file in the codec


    def process_ensemble(self, sender, ens):
        print(str(ens.EnsembleData.EnsembleNumber))
        # Take decoded data and store it

        # Make a dataframe
        df = pd.DataFrame(ens.Correlation.Correlation)
        print(df.head())

    def process_file(self, file_path):
        # Open the file
        with open(file_path, "rb") as file:         # Open file
            bytes_read = file.read(1024)            # Read data from file
            while bytes_read:
                self.codec.add(bytes_read)          # Pass data to codec
                bytes_read = file.read(1024)        # Read data from file






