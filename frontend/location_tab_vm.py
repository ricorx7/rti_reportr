from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWebEngineWidgets, QtCore
import os
from .location_tab_view import Ui_Location_Tab
from rti_python.Writer.rti_projects import RtiProjects
from rti_python.Writer.rti_sql import rti_sql
from gmplot.gmplot import gmplot

import pandas as pd
from tabulate import tabulate

class LocationTabVM(Ui_Location_Tab, QWidget):

    def __init__(self, parent, project_idx, project_name, sql_conn_str):
        Ui_Location_Tab.__init__(self)
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent

        cur_folder = os.path.split(os.path.abspath(__file__))[0]
        cur_folder = os.path.join(cur_folder, '../')            # Move back a director
        cur_folder = os.path.join(cur_folder, 'html')           # html folder
        cur_folder = os.path.join(cur_folder, 'map_' + project_name + '.html')

        # Upgrade it to a Web engine
        # Display the plot
        self.htmlWidget = QtWebEngineWidgets.QWebEngineView(self.htmlWidget)
        self.htmlWidget.resize(700, 565)
        self.htmlWidget.load(QtCore.QUrl().fromLocalFile(cur_folder))

        # sql string
        self.sql_conn_str = sql_conn_str

        print(project_idx)
        self.project_name = project_name
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

            ens_query = 'SELECT ensembles.ensnum, nmea.latitude, nmea.longitude FROM ensembles INNER JOIN nmea ON ensembles.id = nmea.ensindex WHERE ensembles.project_id = %s ORDER BY ensembles.ensnum ASC;'
            sql.cursor.execute(ens_query, (idx,))
            lat_lon_results = sql.cursor.fetchall()
            sql.conn.commit()

            latitude = []
            longitude = []

            for lat_lon in lat_lon_results:
                self.summaryTextEdit.append(str(lat_lon))
                latitude.append(lat_lon[1])
                longitude.append(lat_lon[2])

            lat_lon_end = len(longitude) - 1
            lat_lon_center = int(len(longitude) / 2)
            if lat_lon_center < 0:
                lat_lon_center = 0

            file_name = 'map_' + self.project_name + '.html'
            file_name = os.path.join('html', file_name)

            if not os.path.exists(file_name):
                gmap = gmplot.GoogleMapPlotter(latitude[lat_lon_center], longitude[lat_lon_center], 14)
                gmap.marker(latitude[0], longitude[0], color='r', title="START")
                gmap.marker(latitude[lat_lon_end], longitude[lat_lon_end], color='b', title="END")
                #gmap.scatter(latitude, longitude, 'r', size=40, marker=False)
                gmap.heatmap(latitude, longitude)

                gmap.draw(file_name, api='AIzaSyCMBi5WpMxEVhTu3iVKwsc8NRedgoSVtag', title=('RTI - ' + self.project_name))

        except Exception as e:
            print("Unable to run query", e)
            return

        # Close connection
        sql.close()







