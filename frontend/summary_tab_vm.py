from PyQt5.QtWidgets import QWidget
from .summary_tab_view import Ui_Summary_Tab
from rti_python.Writer.rti_projects import RtiProjects
from rti_python.Writer.rti_sql import rti_sql

import pandas as pd
from tabulate import tabulate

class SummaryTabVM(Ui_Summary_Tab, QWidget):

    def __init__(self, parent, project_idx, project_name, sql_conn_str):
        Ui_Summary_Tab.__init__(self)
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent

        # sql string
        self.sql_conn_str = sql_conn_str

        print(project_idx)
        self.projectLabel.setText(project_name)

        self.first_ens_num = 0
        self.last_ens_num = 0
        self.num_ensembles = 0
        self.first_ens_time = None
        self.last_ens_time = None
        self.serialnumber = ""
        self.firmware = ""

        self.get_project_info(project_idx)

    def get_project_info(self, idx):

        # Make connection
        try:
            sql = rti_sql(self.sql_conn_str)
        except Exception as e:
            print("Unable to connect to the database: ", e)
            return

        # Get all projects
        try:
            # Get all the ensembles for the project
            ens_query = 'SELECT ensnum, datetime, serialnumber, firmware, burstnum FROM ensembles WHERE project_id = %s ORDER BY ensnum ASC;'
            sql.cursor.execute(ens_query, (idx,))
            #ens_results = sql.cursor.fetchall()
            #sql.conn.commit()
            #print(ens_results)

            df = pd.DataFrame(sql.cursor.fetchall(), columns=['ensnum', 'datetime', 'serialnumber', 'firmware', 'BurstNum'])
            self.serialnumber = df['serialnumber'][0]
            self.firmware = df['firmware'][0]
            self.num_ensembles = len(df.index)
            df = df.drop('serialnumber', 1)
            df = df.drop('firmware', 1)     # 1 = column drop

            # Number of bursts
            ens_query = 'SELECT COUNT(DISTINCT BurstNum) FROM ensembles'
            sql.cursor.execute(ens_query, (idx,))
            num_bursts = sql.cursor.fetchall()[0][0]

            self.summaryTextEdit.append(tabulate(df, headers='keys', tablefmt='psql', showindex=False))     # Tabulate to pretty print
            self.summaryTextEdit.append("Serial Number:        {0}".format(self.serialnumber))
            self.summaryTextEdit.append("Firmware Version:     {0}".format(self.firmware))
            self.summaryTextEdit.append("First DateTime:       {0}".format(df['datetime'][0]))
            self.summaryTextEdit.append("Last DateTime:        {0}".format(df['datetime'][len(df.index)-1]))
            self.summaryTextEdit.append("Number of Ensembles:  {0}".format(self.num_ensembles))
            self.summaryTextEdit.append("Number of Bursts:     {0}".format(num_bursts))

        except Exception as e:
            print("Unable to run query", e)
            return

        # Close connection
        sql.close()







