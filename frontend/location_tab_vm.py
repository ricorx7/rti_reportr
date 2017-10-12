from PyQt5.QtWidgets import QWidget
from .location_tab_view import Ui_Location_Tab
from rti_python.Writer.rti_projects import RtiProjects
from rti_python.Writer.rti_sql import rti_sql
import gmplot

import pandas as pd
from tabulate import tabulate

class LocationTabVM(Ui_Location_Tab, QWidget):

    def __init__(self, parent, project_idx, project_name, sql_conn_str):
        Ui_Location_Tab.__init__(self)
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent

        # sql string
        self.sql_conn_str = sql_conn_str

        print(project_idx)
        self.projectLabel.setText(project_name)

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
            #ens_query = '(SELECT id FROM ensembles WHERE project_id = %s ORDER BY ensnum ASC)'
            #lat_lon_query = 'SELECT latitude, longitude FROM nmea WHERE ensindex IN {0};'.format(ens_query)                 # First two will get lat,lon within ensemble number
            #sql.cursor.execute(lat_lon_query, (idx,))

            ens_query = 'SELECT ensembles.id, nmea.latitude, nmea.longitude FROM ensembles INNER JOIN nmea ON ensembles.id = nmea.ensindex WHERE ensembles.project_id = %s;'
            #lat_lon_query = 'SELECT ensindex, n1.latitude, n1.longitude FROM nmea WHERE ensindex IN {0}'.format(ens_query)                 # First two will get lat,lon within ensemble number
            #join_query = '{0} INNER JOIN (SELECT id, ensnum FROM ensembles GROUP BY id) n2 ON (n1.ensindex = n2.id);'.format(lat_lon_query)
            #print(join_query)
            sql.cursor.execute(ens_query, (idx,))
            lat_lon_results = sql.cursor.fetchall()
            sql.conn.commit()
            #print(lat_lon_results)
            for lat_lon in lat_lon_results:
                self.summaryTextEdit.append(str(lat_lon))

        except Exception as e:
            print("Unable to run query", e)
            return

        # Close connection
        sql.close()







