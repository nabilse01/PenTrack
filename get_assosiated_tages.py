import psycopg2  # Importing psycopg2 library to work with PostgreSQL
import pandas as pd
import csv
import  datetime

# Define a function called Delete_FP that takes floor_id, DB_IP, DB_User, DB_PW, DB_name, and DB_port as parameters


def tags_id():
    DB_IP = '192.168.2.31'  # IP address of the database
    DB_User = 'test'  # username to login to the database
    DB_PW = 'Penguineerstest'  # password to login to the database
    DB_name = 'PenDB_Saad'  # name of the database
    DB_port = '5432'  # port number of the database




    # Define a function called Delete_FP that takes floor_id, DB_IP, DB_User, DB_PW, DB_name, and DB_port as parameters


    try:
        global conn  # Declaring 'conn' as a global variable

        # Establish a connection to the PostgreSQL database using the provided credentials
        conn = psycopg2.connect(
            user=DB_User,  # Username for PostgreSQL
            password=DB_PW,  # Password for PostgreSQL
            host=DB_IP,  # Host IP address of the PostgreSQL server
            port=DB_port,  # Port number of the PostgreSQL server
            database=DB_name  # Name of the database to connect to
        )
        cur = conn.cursor()
        cursor = conn.cursor()
        # Open CSV file and skip header row if present
      
            # Iterate through each row in the CSV file
          

        cursor.execute("SELECT tag_id FROM penguin.tbltag_people_assignment")
        tbltag_people_assignment = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT tag_id FROM penguin.tbltag_asset_assignment")
        tbltag_asset_assignment = [row[0] for row in cursor.fetchall()]

        tbltag_combined = tbltag_people_assignment + tbltag_asset_assignment
        return tbltag_combined



    except (Exception, psycopg2.Error) as error:  # Catch any exceptions or errors
        print(error)  # Print the error message if any occurs


tags_id()