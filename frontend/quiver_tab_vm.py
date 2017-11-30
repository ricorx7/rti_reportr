from __future__ import division

import os

from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore, QtGui

import numpy as np
import pandas as pd
import math
import glob

from .quiver_tab_view import Ui_Quiver_Tab

from rti_python.Writer.rti_sql import rti_sql
from rti_python.Plots.rti_sql_plot_mag_dir import plot_mag_dir


class QuiverTabVM(Ui_Quiver_Tab, QWidget):

    def __init__(self, parent, project_idx, project_name, sql_conn_str):
        Ui_Quiver_Tab.__init__(self)
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.sql_conn_str = sql_conn_str
        self.project_idx = project_idx

        print(project_idx)
        self.project_name = project_name
        self.projectLabel.setText(project_name)

        self.cur_folder = os.path.split(os.path.abspath(__file__))[0]
        self.cur_folder = os.path.join(self.cur_folder, '../')            # Move back a director
        self.cur_folder = os.path.join(self.cur_folder, 'html')           # html folder

        self.redrawButton.clicked.connect(self.redraw_plot)

        # Create summary tab
        self.summaryTextEdit = QtWidgets.QTextEdit(self.tabWidget)
        self.summaryTextEdit.setGeometry(QtCore.QRect(0, 70, 761, 131))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.summaryTextEdit.setFont(font)
        self.summaryTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.summaryTextEdit.setReadOnly(True)
        self.summaryTextEdit.setTabStopWidth(86)
        self.summaryTextEdit.setObjectName("summaryTextEdit")

        # Draw the plot
        self.draw_plots()

    def draw_plots(self):
        # Clear the current tab
        self.tabWidget.clear()

        # Add Summary Tab
        self.tabWidget.addTab(self.summaryTextEdit, 'Summary')

        # Get the ADCP configurations
        configs_df = self.get_adcp_configs(self.project_idx)

        if not configs_df.empty:
            for index, row in configs_df.iterrows():
                self.draw_plot(row['subsystemcode'], row['subsystemconfig'])

    def redraw_plot(self):
        # Remove the old files
        for fl in glob.glob(os.path.join(self.cur_folder, self.project_name + '*' + '_combined_vector.html')):
            os.remove(fl)
        for fl in glob.glob(os.path.join(self.cur_folder, self.project_name + '*' + '_vector.html')):
            os.remove(fl)
        for fl in glob.glob(os.path.join(self.cur_folder, self.project_name + '*' + '_mag.html')):
            os.remove(fl)

        # Clear the summary tab
        self.summaryTextEdit.clear()

        # Redraw the plots
        self.draw_plots()

    def draw_plot(self, ss_code, ss_config):
        # Create file names
        ss_str = "_{}_{}".format(ss_config, ss_code)
        combined_vector_file = os.path.join(self.cur_folder, self.project_name + ss_str + '_combined_vector.html')
        vector_file = os.path.join(self.cur_folder, self.project_name + ss_str + '_vector.html')
        mag_file = os.path.join(self.cur_folder, self.project_name + ss_str + '_mag.html')

        # Get data from DB
        adcp = self.get_adcp_info(self.project_idx)
        earth_vel_east_df = self.get_project_velocity(self.project_idx, 0, ss_code=ss_code, ss_config=ss_config)  # Each row is an ensemble
        earth_vel_north_df = self.get_project_velocity(self.project_idx, 1, ss_code=ss_code, ss_config=ss_config)

        # If there is no data, than we cannot plot
        if earth_vel_north_df.empty or earth_vel_east_df.empty:
            return

        self.summaryTextEdit.append("***   ADCP Data   ***")
        self.summaryTextEdit.append(str(adcp))

        # Check if upward or downward
        is_upward = self.is_adcp_up_facing(self.project_idx)
        if is_upward:
            self.summaryTextEdit.append('ADCP Is Upward Facing')
        else:
            self.summaryTextEdit.append('ADCP Is Downward Facing')

        # Drop all vertical beam data
        if earth_vel_east_df is not None and not earth_vel_east_df.empty:
            earth_vel_east_df = earth_vel_east_df[earth_vel_east_df.numbeams > 1]
        if earth_vel_north_df is not None and not earth_vel_north_df.empty:
            earth_vel_north_df = earth_vel_north_df[earth_vel_north_df.numbeams > 1]

        # Bottom Track range
        bottom_track_range_df = self.get_bt_range(self.project_idx, ss_code=ss_code, ss_config=ss_config)

        # If they were already created, do no work
        if not os.path.exists(combined_vector_file) or not os.path.exists(vector_file) or not os.path.exists(mag_file):

            # Mark bad below bottom
            # THIS IS DONE BY SETTING max_vel
            earth_vel_east_df, earth_vel_north_df, num_bins = self.mark_bad_below_bottom(self.project_idx, earth_vel_east_df, earth_vel_north_df)

            # Create the plot
            plot_mag_dir(self.project_name, adcp, earth_vel_east_df, earth_vel_north_df, num_bins, bt_range_df=bottom_track_range_df, ss_code=ss_code, ss_config=ss_config, max_vel=2.0, flip_y_axis=is_upward, smoothing="hamming", smoothing_win=50)

        # Upgrade it to a Web engine
        # Display the plot
        htmlWidget = QtWebEngineWidgets.QWebEngineView(self.tabWidget)
        htmlWidget.load(QtCore.QUrl().fromLocalFile(combined_vector_file))

        htmlMagWidget = QtWebEngineWidgets.QWebEngineView(self.tabWidget)
        htmlMagWidget.load(QtCore.QUrl().fromLocalFile(mag_file))

        htmlVectorWidget = QtWebEngineWidgets.QWebEngineView(self.tabWidget)
        htmlVectorWidget.load(QtCore.QUrl().fromLocalFile(vector_file))

        # Add the tabs
        self.tabWidget.addTab(htmlWidget, "Combined" + ss_str)
        self.tabWidget.addTab(htmlMagWidget, "Water Magnitude" + ss_str)
        self.tabWidget.addTab(htmlVectorWidget, "Water Vectors" + ss_str)

    def get_project_velocity(self, idx, beam, ss_code=None, ss_config=None, remove_ship_speed=True):
        """
        Get the earth velocity for the project info from the database.
        :param idx: Project index.
        :param beam: Beam number.
        :param ss_code: Subsystem code.
        :param ss_config: Subsystem configuration index.
        :param remove_ship_speed: Remove the ship speed from the velocities.
        :return: Earth velocity data.
        """

        # Make connection
        try:
            sql = rti_sql(self.sql_conn_str)
        except Exception as e:
            print("Unable to connect to the database: ", e)
            return

        # Get ensemble earth velocity data
        earth_vel = sql.get_earth_vel_data(idx, beam, ss_code=ss_code, ss_config=ss_config)

        # Verify we have data
        if earth_vel is not None and not earth_vel.empty:

            num_bins = earth_vel['numbins'][0]

            if remove_ship_speed:
                # Get bottom track velocity
                bt_vel = sql.get_bottom_track_vel(idx)

                # Verify there is bottom track data
                if not bt_vel.empty:

                    num_bins = bt_vel['numbins'][0]

                    # Mark all bad data 0 so when added, it will not increase above 88.888
                    #bt_vel = bt_vel.replace([88.888], 0.0)
                    #earth_vel = earth_vel.replace([88.888], 0.0)

                    for bin_loc in range(num_bins):
                        bin_str = 'bin' + str(bin_loc)

                        # Add bottom track velocity to earth velocity to remove the ship speed
                        if beam == 0:
                            earth_vel[bin_str] += bt_vel['Earth0']
                        elif beam == 1:
                            earth_vel[bin_str] += bt_vel['Earth1']
                        elif beam == 2:
                            earth_vel[bin_str] += bt_vel['Earth2']
                        elif beam == 3:
                            earth_vel[bin_str] += bt_vel['Earth3']

                    """
                    earth_vel[earth_vel.beam == 0] += bt_vel['Earth0']
                    earth_vel[earth_vel.beam == 1] += bt_vel['Earth1']
                    earth_vel[earth_vel.beam == 2] += bt_vel['Earth2']
                    earth_vel[earth_vel.beam == 3] += bt_vel['Earth3']
                    """

                    self.summaryTextEdit.append("***   Bottom Track Velocity   ***")
                    self.summaryTextEdit.append(str(bt_vel))

            if beam == 0:
                self.summaryTextEdit.append("***   Earth Velocity - East[{}_{}_{}]   ***".format(beam, ss_code, ss_config))
            elif beam == 1:
                self.summaryTextEdit.append("***   Earth Velocity - North[{}_{}_{}]   ***".format(beam, ss_code, ss_config))
            elif beam == 2:
                self.summaryTextEdit.append("***   Earth Velocity - Vertical[{}_{}_{}]   ***".format(beam, ss_code, ss_config))
            elif beam == 3:
                self.summaryTextEdit.append("***   Earth Velocity - Error[{}_{}_{}]   ***".format(beam, ss_code, ss_config))
            self.summaryTextEdit.append(str(earth_vel.iloc[:, :num_bins+4]))        # Add 4 to include the [ensnum, numbeams, numbins, beam]

        sql.close()

        return earth_vel

    def get_adcp_info(self, idx):
        """
        Get the ADCP info.
        :param idx: Project index.
        :return: ADCP info.
        """

        # Make connection
        try:
            sql = rti_sql(self.sql_conn_str)
        except Exception as e:
            print("Unable to connect to the database: ", e)
            return

        # Get ADCP data
        info = sql.get_adcp_info(idx)

        sql.close()

        return info

    def is_adcp_up_facing(self, idx):
        """
        Get the ADCP info.
        :param idx: Project index.
        :return: ADCP info.
        """

        # Make connection
        try:
            sql = rti_sql(self.sql_conn_str)
        except Exception as e:
            print("Unable to connect to the database: ", e)
            return

        # Get ADCP data
        compass_df = sql.get_compass_data(idx)

        sql.close()

        self.summaryTextEdit.append('*** Compass Data ***')
        self.summaryTextEdit.append(str(compass_df))

        # Take the Absolute value
        compass_df['roll'] = abs(compass_df['roll'])
        avg_roll = compass_df['roll'].mean()

        print("Average Roll: ", avg_roll)

        # Angles around 180 deg is downward looking
        # Angles around 0 deg is upward looking
        # Angles will be +/-  so +/180 degrees is downward
        if 130.0 < avg_roll <= 180.0:
            print("Downward facing")
            return False

        print("Upward facing")
        return True

    def get_adcp_configs(self, idx):
        """
        Get the ADCP configurations.
        :param idx: Project index.
        :return: ADCP configurations.
        """

        # Make connection
        try:
            sql = rti_sql(self.sql_conn_str)
        except Exception as e:
            print("Unable to connect to the database: ", e)
            return

        # Get ADCP data
        ss_configs = sql.get_subsystem_configs(idx)

        sql.close()

        #self.summaryTextEdit.append('*** Subsystem Codes ***')
        #self.summaryTextEdit.append(str(ss_codes))
        self.summaryTextEdit.append('*** Subsystem Configuration ***')
        self.summaryTextEdit.append(str(ss_configs))

        return ss_configs

    def mark_bad_below_bottom(self, idx, east_vel, north_vel):
        # Make connection
        try:
            sql = rti_sql(self.sql_conn_str)
        except Exception as e:
            print("Unable to connect to the database: ", e)
            return

        # Get ensemble earth velocity data
        ranges = sql.get_bottom_track_range(idx)

        sql.close()

        # No bottom track data so do nothing
        if ranges.empty:
            return east_vel, north_vel, 0

        num_beams = ranges['NumBeams'][0]
        num_bins = ranges['NumBins'][0]
        bin_size = ranges['BinSize'][0]
        first_bin = ranges['RangeFirstBin'][0]
        num_ens = len(ranges.index)
        max_bin_depth = 0

        for ens in range(num_ens):

            # Depth
            avg_depth = 0.0
            count = 0
            for beam in range(num_beams):
                range_str = 'RangeBeam' + str(beam)
                if ranges[range_str][ens] is not 88.888:
                    avg_depth += ranges[range_str][ens]
                    count += 1

            if count > 0:
                avg_depth = avg_depth / count

            bin_depth = int(round((avg_depth - first_bin) / bin_size, 0))
            max_bin_depth = max(bin_depth, max_bin_depth)                       # Keep track of the largest bin depth

            #if 0 < bin_depth < num_bins:
                #for bin_loc in range(bin_depth-1, num_bins):
                #    bin_str = 'bin' + str(bin_loc)
                #    east_vel.iloc[ens][bin_str] = 0.0
                #    north_vel.iloc[ens][bin_str] = 0.0

                #bin_list = []
                #for bin_loc in range(bin_depth - 1, num_bins):
                #    bin_str = 'bin' + str(bin_loc)
                #    east_vel.loc[ens][bin_str] = 0.0
                #    north_vel.loc[ens][bin_str] = 0.0

        return east_vel, north_vel, max_bin_depth

    def get_bt_range(self, idx, ss_code=None, ss_config=None):
        """
        Get the earth velocity for the project info from the database.
        :param idx: Project index.
        :param beam: Beam number.
        :param ss_code: Subsystem code.
        :param ss_config: Subsystem configuration index.
        :return: Average range for each ensemble.
        """

        # Make connection
        try:
            sql = rti_sql(self.sql_conn_str)
        except Exception as e:
            print("Unable to connect to the database: ", e)
            return

        # Get ensemble Bottom Track Range data
        bt_range_df = sql.get_bottom_track_range(idx, ss_code=ss_code, ss_config=ss_config)

        # Verify we have data
        if bt_range_df is not None and not bt_range_df.empty:
            # Set all column values that are 0 to NaN so average will
            # Only calculate good values
            bt_range_df = bt_range_df.replace(0, np.NAN)

            # Average the columns
            bt_range_df['avg'] = bt_range_df[['RangeBeam0', 'RangeBeam1', 'RangeBeam2', 'RangeBeam3']].mean(axis=1)

            # Bin number for the range
            bt_range_df['BinRange'] = (bt_range_df['avg'] - bt_range_df['RangeFirstBin']) / bt_range_df['BinSize']

            self.summaryTextEdit.append("***   Bottom Track Range   ***")
            self.summaryTextEdit.append(str(bt_range_df))

        sql.close()

        return bt_range_df
