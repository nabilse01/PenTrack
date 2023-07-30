import psycopg2  # Importing psycopg2 library to work with PostgreSQL
import pandas as pd 
import random
# Define a function called Delete_FP that takes floor_id, DB_IP, DB_User, DB_PW, DB_name, and DB_port as parameters
df = pd.read_csv('people_with_department_id.csv')

def uplode_fp():
    DB_IP = '192.168.2.31'  # IP address of the database
    DB_User = 'test'  # username to login to the database
    DB_PW = 'Penguineerstest'  # password to login to the database
    DB_name = 'PenDB_Saad'  # name of the database
    DB_port = '5432'  # port number of the database

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

# Open CSV file and skip header row if present

        cur.execute("SELECT * FROM penguin.tblpeople")
        rows = cur.fetchall()

        # Iterate through the rows and update the department_id column
        for row in rows:
            department_id = random.randint(1, 5)
            cur.execute("UPDATE penguin.tblpeople SET department_id = %s WHERE id = %s", (department_id, row[0]))

        # Commit the changes made to the database
        conn.commit()
    # Commit the transaction

    except (Exception, psycopg2.Error) as error:  # Catch any exceptions or errors
        print(error)  # Print the error message if any occurs
uplode_fp()