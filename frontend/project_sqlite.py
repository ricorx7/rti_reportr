import sqlite3 as sqlite3
from sqlite3 import Error
import os as os


class Project:

    def __init__(self, db_file):
        # Init connection
        self.conn = None

        # Create the database file
        # If this is a new database file, create the tables
        self.create_conn(db_file)


    def create_conn(self, db_file):

        # If the file does not exist, then we need to create the tables
        new_file = True
        if os.path.isfile(db_file):
            new_file = False

        try:
            # Create a database connection to a SQLite database
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)

            # If a new file, create the tables
            if new_file:
                self.create_tables()

        except Error as e:
            print(e)
            return None

    def close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()

    def create_tables(self):
        c = self.conn.cursor()              # Create connection

        # Creating a new SQLite table for Projects
        c.execute('CREATE TABLE Projects (Name TEXT)')

        # Creating a new SQLite table for Ensembles
        c.execute('CREATE TABLE {tn} ({nf} {ft})'.format(tn='Ensembles', nf='Project', ft='INTEGER'))               # Project index
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}".format(tn='Ensembles', cn='Correlation', ct='BLOB'))    # Pickle data
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}".format(tn='Ensembles', cn='Amplitude', ct='BLOB'))      # Pickle data
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}".format(tn='Ensembles', cn='BeamVel', ct='BLOB'))        # Pickle data

        self.conn.commit()
