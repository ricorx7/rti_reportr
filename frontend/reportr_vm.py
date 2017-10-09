import datetime
import os
import sys
from .reportr_view import Ui_RoweTechReportR
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .project_sqlite import Project



from rti_python.Writer.rti_sql import rti_sql
from rti_python.Writer.rti_projects import RtiProjects

import pandas as pd

class ReportrVM(Ui_RoweTechReportR):
    """

    """

    def __init__(self, parent):
        # Place the Import here because this import is also done within rti_python
        # which is causing it to overlap
        import rti_python.Codecs.AdcpCodec as codec
        import rti_python.Writer.rti_h5py as h5py

        Ui_RoweTechReportR.__init__(self)
        self.setupUi(parent)
        self.parent = parent

        self.project_name = 'Project1'

        # Create project file
        #self.project_file = Project("projects.sqlite")

        # Create project h5py file
        # self.h5py_file = h5py.RtiH5py("project.h5py")

        self.projects = RtiProjects(host='localhost',
                                    port='5432',
                                    dbname='rti',
                                    user='test',
                                    pw='123456')

        for prj in self.projects.get_all_projects():
            self.projectListWidget.addItem(prj[1])

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

    def read_files(self, give_warning=False):
        """
        Create a project.
        If project is taken, ask for a new project.

        Decode the ADCP data from the file path given
        :return:
        """
        display_txt = "Project Name: "
        if give_warning:
            display_txt = "Project Name already used.  Please give a new project name: "

        # Display a dialog box to get a project name
        text, okPressed = QInputDialog.getText(self.parent, "Project Name", display_txt, QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
            self.project_name = text

            # Get the index for the project in the DB
            is_prj_added = self.projects.add_prj_sql(text)

            if is_prj_added:
                # Read in the data and decode it
                print("Reading files...")
                for x in range(self.selectedFileListView.count()):              # Load each file selected
                    file = str(self.selectedFileListView.item(x).text())        # Get the file path from the list
                    print("Loading: ", file)
                    self.process_file(file)                                     # Process the file in the codec

                    # Add the project to the list
                    self.projectListWidget.addItem(self.project_name)
            else:
                # Ask for a new project
                self.read_files(True)

    def process_file(self, file_path):
        # Start a batch insert in to the table
        self.projects.begin_batch(self.project_name)

        # Open the file
        with open(file_path, "rb") as file:         # Open file
            bytes_read = file.read(1024)            # Read data from file
            while bytes_read:
                self.codec.add(bytes_read)          # Pass data to codec
                bytes_read = file.read(1024)        # Read data from file

        # End the batch insert
        self.projects.end_batch()

    def process_ensemble(self, sender, ens):
        print("ReportR_vm.process_ensemble() Ens Num: " + str(ens.EnsembleData.EnsembleNumber))
        # Take decoded data and store it

        # Create an empty dataframe
        ens_df = pd.DataFrame()

        # Each Beam creates a new column for all the data

        # Make a dataframe
        df = pd.DataFrame(ens.Amplitude.Amplitude)
        print(df.head())

        # Add the ensemble to the project
        self.projects.add_ensemble(ens)








