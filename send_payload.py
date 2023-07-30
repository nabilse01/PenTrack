import time
from json import dumps
from kafka import KafkaProducer
import psycopg2  # Importing psycopg2 library to work with PostgreSQL
import random
from datetime import datetime
from shapely.geometry import Point, Polygon


# Set the topic name for Kafka producer
topic_name = 'hello_world5'

# Create a KafkaProducer object with bootstrap servers and value serializer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

# Define source and type as strings
source = str('directPosition')
type = str('position')


DB_IP = '192.168.2.31'  # IP address of the database
DB_User = 'test'  # username to login to the database
DB_PW = 'Penguineerstest'  # password to login to the database
DB_name = 'PenDB_Saad'  # name of the database
DB_port = '5432'  # port number of the database

# Establish a connection to the PostgreSQL database using the provided credentials
global conn
conn = psycopg2.connect(
    user=DB_User,  # Username for PostgreSQL
    password=DB_PW,  # Password for PostgreSQL
    host=DB_IP,  # Host IP address of the PostgreSQL server
    port=DB_port,  # Port number of the PostgreSQL server
    database=DB_name  # Name of the database to connect to
)


# Function to retrieve tags from the database
def get_tags():
    # Initialize an empty list for the tags
    tags = []

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute SQL query to select mac addresses from tbltags table
    # that are assigned to either people or assets
    # and have an update status other than 2
    cursor.execute("""
        SELECT mac 
        FROM penguin.tbltags 
        WHERE id IN (
            SELECT tag_id 
            FROM penguin.tbltag_people_assignment

            UNION 

            SELECT tag_id 
            FROM penguin.tbltag_asset_assignment
        )
        AND update_status != 2
    """)

    # Fetch all the results of the query
    results = cursor.fetchall()

    # Extract the mac addresses from the results and add them to the tags list
    tags = [row[0] for row in results]

    # Return the tags list
    return tags


# Function to retrieve floor information from the database
def get_floors_info():
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # SQL query to select floor id, x-coordinate, and y-coordinate
    # from tblfloors, tblzones, tblpolygon_points and tblpolygon_type tables
    # where floors have an update status other than 2,
    # zones have zone_name 'Coverage Area', zone update status other than 2,
    # and polygon type description is 'zone'
    query = """
        SELECT f.id, p.x, p.y
        FROM penguin.tblfloors AS f
        JOIN penguin.tblzones AS z ON f.id = z.floor_id
        JOIN penguin.tblpolygon_points AS p ON p.reference_id = z.id
        JOIN penguin.tblpolygon_type AS pt ON p.type_id = pt.id
        WHERE f.update_status != 2 
        AND z.zone_name = 'Coverage Area' 
        AND z.update_status != 2
        AND pt.description = 'zone'
        ORDER BY p.order_index
    """

    # Execute the SQL query
    cursor.execute(query)

    # Fetch all the results of the query
    results = cursor.fetchall()

    # Create an empty dictionary to store floor information
    floor_info = {}

    # Iterate over the returned results
    for floor_id, x, y in results:
        # Check if the floor id is not already present in the dictionary
        if floor_id not in floor_info:
            # Use None as placeholder (no need for a tuple with empty lists)
            floor_info[floor_id] = None

        # Add coordinates to the list associated with the floor id
        if floor_info[floor_id] is None:
            floor_info[floor_id] = []

        floor_info[floor_id].append((x, y))

    # Create polygons using the coordinate lists for each floor id
    for floor_id, coords in floor_info.items():
        # Store the Polygon object in the floor_info dictionary
        floor_info[floor_id] = Polygon(coords)

    # Return the floor_info dictionary with floor id as keys and Polygon objects as values
    return floor_info


# Store initial values
tags = get_tags()
floor_info = get_floors_info()


def generate_location(TagMac, floor_info):
    # Choose a random key from the floor_info dictionary
    random_key = random.choice(list(floor_info.keys()))
    # Get the corresponding value of the random key
    random_value = floor_info[random_key]

    # Generate random x and y coordinates within the bounds of the polygon
    point = None
    while not random_value.contains(point):
        # Generate random x and y coordinates within the boundaries of the polygon
        X = random.uniform(random_value.bounds[0], random_value.bounds[2])
        Y = random.uniform(random_value.bounds[1], random_value.bounds[3])
        point = Point(X, Y)

    # Get the current timestamp
    TimeStamp = int(datetime.timestamp(datetime.now()))

    return {
        "TagMac": TagMac,
        "TimeStamp": TimeStamp,
        "FloorId": random_key,
        "X": X,
        "Y": Y
    }


while True:
    # Get the current transaction time
    transactionTime = str(datetime.now())

    # Generate payload for each tag using the generate_location function
    data = [generate_location(tag, floor_info) for tag in tags]

    # Split the data into two halves
    half_length = len(data) // 2
    data1 = data[:half_length]
    data2 = data[half_length:]

    # Create payload dictionaries for both halves
    start_time = datetime.now()
    payload1 = {
        "source": source,
        "type": type,
        "transactionTime": transactionTime,
        "data": data1
    }

    payload2 = {
        "source": source,
        "type": type,
        "transactionTime": transactionTime,
        "data": data2
    }

    # Send both payloads to the specified topic using a producer
    producer.send(topic_name, value=payload1)
    producer.send(topic_name, value=payload2)

    # Wait for a specific amount of time before repeating the process
    time.sleep(.75)

    end_time = datetime.now()
    time_taken = end_time - start_time
    print("Time taken:", time_taken)
