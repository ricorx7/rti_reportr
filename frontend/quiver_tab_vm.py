from __future__ import division

import os

from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWebEngineWidgets, QtCore

import numpy as np
import pandas as pd
import math

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, save, output_file
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.transform import transform

from .quiver_tab_view import Ui_Quiver_Tab

from rti_python.Writer.rti_sql import rti_sql


class QuiverTabVM(Ui_Quiver_Tab, QWidget):

    def __init__(self, parent, project_idx, project_name, sql_conn_str):
        Ui_Quiver_Tab.__init__(self)
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.sql_conn_str = sql_conn_str

        print(project_idx)
        self.project_name = project_name
        self.projectLabel.setText(project_name)

        cur_folder = os.path.split(os.path.abspath(__file__))[0]
        cur_folder = os.path.join(cur_folder, '../')            # Move back a director
        cur_folder = os.path.join(cur_folder, 'html')           # html folder
        cur_folder = os.path.join(cur_folder, 'vector_' + project_name + '.html')

        adcp = self.get_adcp_info(project_idx)
        earth_vel_east_df = self.get_project_velocity(project_idx, 0)       # Each row is an ensemble
        earth_vel_north_df = self.get_project_velocity(project_idx, 1)

        #print(earth_vel_east_df.head())
        #print(earth_vel_north_df.head())

        # Create the plot
        self.create_plot(adcp, earth_vel_east_df, earth_vel_north_df)

        # Upgrade it to a Web engine
        # Display the plot
        self.htmlWidget = QtWebEngineWidgets.QWebEngineView(self.htmlWidget)
        self.htmlWidget.resize(700, 565)
        self.htmlWidget.load(QtCore.QUrl().fromLocalFile(cur_folder))

    def create_plot(self, adcp, earth_vel_east_df, earth_vel_north_df):
        # BAD VELOCITY
        BAD_VEL = 88.888

        # Scale factor to allow the quivers to fit on the screen
        SCALE_FACTOR = 4

        # Get the number of bins in the df
        # Get the number of ensembles in the df
        num_bins = adcp['numbins']
        num_ens = len(earth_vel_east_df.index)

        xx = np.linspace(0, num_ens, num=num_ens)
        yy = np.linspace(0, num_ens, num=num_ens)

        x0_ens = []
        y0_ens = []
        x1_ens = []
        y1_ens = []
        length_vals = []
        speed_vals = []

        df_mag = pd.DataFrame()

        for ens_loc in range(num_ens):

            mag_vals = []
            dir_vals = []

            for bin_loc in range(num_bins):
                bin_str = 'bin'+str(bin_loc)

                u = 0.0
                v = 0.0
                if earth_vel_east_df.iloc[ens_loc][bin_str] != BAD_VEL and earth_vel_north_df.iloc[ens_loc][bin_str] != BAD_VEL:
                    u = earth_vel_east_df.iloc[ens_loc][bin_str]
                    v = earth_vel_north_df.iloc[ens_loc][bin_str]

                mag = math.sqrt(u*u + v*v)
                mag_vals.append(mag)
                speed_vals.append(mag)
                dir = math.degrees(math.atan2(u, v))
                if dir < 0:
                    dir = 360.0 + dir
                dir_vals.append(dir)

                length_val = mag / SCALE_FACTOR             # Scale the length to fit better on the screen
                length_vals.append(length_val)

                x1_val = ens_loc + length_val * np.cos(dir)
                y1_val = bin_loc + length_val * np.sin(dir)

                x0_ens.append(ens_loc)          # X = ensemble
                y0_ens.append(bin_loc)          # Y = bin
                x1_ens.append(x1_val)           # x1 = length and angle
                y1_ens.append(y1_val)           # y1 = length and angle

            # Store the column for the speed values
            df_mag[str(ens_loc)] = mag_vals

        length = np.asarray(length_vals)
        speed = np.asarray(speed_vals)

        """
        Y, X = np.meshgrid(xx, yy)
        #U = -1 - X ** 2 + Y
        #V = 1 + X - Y ** 2
        U = X
        V = Y
        speed = np.sqrt(U * U + V * V)
        theta = np.arctan(V / U)
        x0 = X[::2, ::2].flatten()
        y0 = Y[::2, ::2].flatten()
        length = speed[::2, ::2].flatten() / 40
        angle = theta[::2, ::2].flatten()
        x1 = x0 + length * np.cos(angle)
        y1 = y0 + length * np.sin(angle)
        xs, ys = self.streamlines(xx, yy, U.T, V.T, density=2)
        """

        #cm = np.array(["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"])  # Green / White / Red
        #cm = np.array(["#C7E9B4", "#7FCDBB", "#41B6C4", "#1D91C0", "#225EA8", "#0C2C84"])      #  Green / Blue
        #cm = np.array(['#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef', '#deebf7', '#f7fbff'])  # Blue to white
        cm = np.array(['#f7fbff', '#deebf7', '#c6dbef', '#6baed6', '#9ecae1', '#4292c6', '#2171b5', '#084594'])  # White to Blue
        ix = ((length - length.min()) / (length.max() - length.min()) * 5).astype('int')
        colors = cm[ix]
        # this is the colormap from the original NYTimes plot
        mapper = LinearColorMapper(palette=cm, low=speed.min(), high=speed.max())
        color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                             ticker=BasicTicker(desired_num_ticks=len(cm)),
                             label_standoff=6, border_line_color=None, location=(0, 0))


        TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

        p1 = figure(x_range=(0, num_ens), y_range=(0, num_bins), tools=TOOLS)
        p1.segment(x0_ens, y0_ens, x1_ens, y1_ens, color=colors, line_width=2)
        #p1.add_layout(color_bar, 'right')

        #p3 = figure(x_range=p1.x_range, y_range=p1.y_range)
        #p3.multi_line(xs, ys, color="#ee6666", line_width=2, line_alpha=0.8)

        speed_df = pd.DataFrame()
        speed_df['speed'] = speed_vals
        speed_df['ens'] = x0_ens
        speed_df['bin'] = y0_ens
        source = ColumnDataSource(speed_df)

        p2 = figure(x_range=p1.x_range, y_range=p1.y_range, tools=TOOLS, toolbar_location='left')
        p2.rect(x='ens', y='bin', width=1, height=1, source=source, fill_color=transform('speed', mapper), line_color=None)
        p2.add_layout(color_bar, 'right')
        p2.select_one(HoverTool).tooltips = [
            ("index", "$index"),
            ("(x,y)", "($x, $y)"),
            ("fill color", "$color[hex, swatch]:fill_color"),
            ('speed', '@speed'),
        ]

        file_name = 'vector_' + self.project_name + '.html'
        file_name = os.path.join('html', file_name)

        output_file(file_name, title="vector.py example")

        # show(gridplot([[p1, p2]], plot_width=400, plot_height=400))  # open a browser
        #save(gridplot([[p1, p2]], plot_width=320, plot_height=530))  # Just save to file
        save(gridplot([[p1, p2]], plot_width=640, plot_height=510))  # Just save to file

    def streamlines(self, x, y, u, v, density=1):
        ''' Return streamlines of a vector flow.

        * x and y are 1d arrays defining an *evenly spaced* grid.
        * u and v are 2d arrays (shape [y,x]) giving velocities.
        * density controls the closeness of the streamlines. For different
          densities in each direction, use a tuple or list [densityx, densityy].

        '''

        # Set up some constants - size of the grid used.
        NGX = len(x)
        NGY = len(y)

        # Constants used to convert between grid index coords and user coords.
        DX = x[1]-x[0]
        DY = y[1]-y[0]
        XOFF = x[0]
        YOFF = y[0]

        # Now rescale velocity onto axes-coordinates
        u = u / (x[-1]-x[0])
        v = v / (y[-1]-y[0])
        speed = np.sqrt(u*u+v*v)
        # s (path length) will now be in axes-coordinates, but we must
        # rescale u for integrations.
        u *= NGX
        v *= NGY
        # Now u and v in grid-coordinates.

        NBX = int(30*density)
        NBY = int(30*density)
        blank = np.zeros((NBY,NBX))

        bx_spacing = NGX/float(NBX-1)
        by_spacing = NGY/float(NBY-1)

        def blank_pos(xi, yi):
            return int((xi / bx_spacing) + 0.5), \
                   int((yi / by_spacing) + 0.5)

        def value_at(a, xi, yi):
            if type(xi) == np.ndarray:
                x = xi.astype(np.int)
                y = yi.astype(np.int)
            else:
                x = np.int(xi)
                y = np.int(yi)
            a00 = a[y,x]
            a01 = a[y,x+1]
            a10 = a[y+1,x]
            a11 = a[y+1,x+1]
            xt = xi - x
            yt = yi - y
            a0 = a00*(1-xt) + a01*xt
            a1 = a10*(1-xt) + a11*xt
            return a0*(1-yt) + a1*yt

        def rk4_integrate(x0, y0):
            # This function does RK4 forward and back trajectories from
            # the initial conditions, with the odd 'blank array'
            # termination conditions. TODO tidy the integration loops.

            def f(xi, yi):
                dt_ds = 1./value_at(speed, xi, yi)
                ui = value_at(u, xi, yi)
                vi = value_at(v, xi, yi)
                return ui*dt_ds, vi*dt_ds

            def g(xi, yi):
                dt_ds = 1./value_at(speed, xi, yi)
                ui = value_at(u, xi, yi)
                vi = value_at(v, xi, yi)
                return -ui*dt_ds, -vi*dt_ds

            check = lambda xi, yi: xi>=0 and xi<NGX-1 and yi>=0 and yi<NGY-1

            bx_changes = []
            by_changes = []

            # Integrator function
            def rk4(x0, y0, f):
                ds = 0.01               # min(1./NGX, 1./NGY, 0.01)
                stotal = 0
                xi = x0
                yi = y0
                xb, yb = blank_pos(xi, yi)
                xf_traj = []
                yf_traj = []
                while check(xi, yi):
                    # Time step. First save the point.
                    xf_traj.append(xi)
                    yf_traj.append(yi)
                    # Next, advance one using RK4
                    try:
                        k1x, k1y = f(xi, yi)
                        k2x, k2y = f(xi + .5*ds*k1x, yi + .5*ds*k1y)
                        k3x, k3y = f(xi + .5*ds*k2x, yi + .5*ds*k2y)
                        k4x, k4y = f(xi + ds*k3x, yi + ds*k3y)
                    except IndexError:
                        # Out of the domain on one of the intermediate steps
                        break
                    xi += ds*(k1x+2*k2x+2*k3x+k4x) / 6.
                    yi += ds*(k1y+2*k2y+2*k3y+k4y) / 6.
                    # Final position might be out of the domain
                    if not check(xi, yi): break
                    stotal += ds
                    # Next, if s gets to thres, check blank.
                    new_xb, new_yb = blank_pos(xi, yi)
                    if new_xb != xb or new_yb != yb:
                        # New square, so check and colour. Quit if required.
                        if blank[new_yb,new_xb] == 0:
                            blank[new_yb,new_xb] = 1
                            bx_changes.append(new_xb)
                            by_changes.append(new_yb)
                            xb = new_xb
                            yb = new_yb
                        else:
                            break
                    if stotal > 2:
                        break
                return stotal, xf_traj, yf_traj

            integrator = rk4

            sf, xf_traj, yf_traj = integrator(x0, y0, f)
            sb, xb_traj, yb_traj = integrator(x0, y0, g)
            stotal = sf + sb
            x_traj = xb_traj[::-1] + xf_traj[1:]
            y_traj = yb_traj[::-1] + yf_traj[1:]

            # Tests to check length of traj. Remember, s in units of axes.
            if len(x_traj) < 1: return None
            if stotal > .2:
                initxb, inityb = blank_pos(x0, y0)
                blank[inityb, initxb] = 1
                return x_traj, y_traj
            else:
                for xb, yb in zip(bx_changes, by_changes):
                    blank[yb, xb] = 0
                return None

        # A quick function for integrating trajectories if blank==0.
        trajectories = []
        def traj(xb, yb):
            if xb < 0 or xb >= NBX or yb < 0 or yb >= NBY:
                return
            if blank[yb, xb] == 0:
                t = rk4_integrate(xb*bx_spacing, yb*by_spacing)
                if t is not None:
                    trajectories.append(t)

        # Now we build up the trajectory set. I've found it best to look
        # for blank==0 along the edges first, and work inwards.
        for indent in range((max(NBX,NBY))//2):
            for xi in range(max(NBX,NBY)-2*indent):
                traj(xi+indent, indent)
                traj(xi+indent, NBY-1-indent)
                traj(indent, xi+indent)
                traj(NBX-1-indent, xi+indent)

        xs = [np.array(t[0])*DX+XOFF for t in trajectories]
        ys = [np.array(t[1])*DY+YOFF for t in trajectories]

        return xs, ys

    def get_project_velocity(self, idx, beam, remove_ship_speed=True):
        """
        Get the earth velocity for the project info from the database.
        :param idx: Project index.
        :param beam: Beam number.
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
        earth_vel = sql.get_earth_vel_data(idx, beam)

        if remove_ship_speed:
            # Get bottom track velocity
            bt_vel = sql.get_bottom_track_vel(idx)

            num_bins = bt_vel['numbins'][0]

            # Mark all bad data 0 so when added, it will not increase above 88.888
            bt_vel = bt_vel.replace([88.888], 0.0)
            earth_vel = earth_vel.replace([88.888], 0.0)

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

        self.summaryTextEdit.append(str(bt_vel))
        self.summaryTextEdit.append(str(earth_vel.iloc[:, :num_bins+2]))

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

        # Get ensemble earth velocity data
        info = sql.get_adcp_info(idx)

        sql.close()

        return info
