# hard hack

import io
import os
import sqlite3
import cv2
import csv

from time import sleep
from time import time
from sqlite3 import Error

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="environ.json"

# Instantiates a client
client = vision.ImageAnnotatorClient()

def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))

    return objects

def capture_image():
    webcam = cv2.VideoCapture(0)
    start = time()
    # key = cv2.waitKey(1)
    while True:
        check, frame = webcam.read()
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        elasped = time() - start
        if elasped >= 1:
            break
    cv2.imwrite(filename='test.jpg', img=frame)
    webcam.release()
    cv2.destroyAllWindows()
    print("Processing image...")

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn
 
 
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_food(conn, food):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO foods (title,expiry_date)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, food)
    return cur.lastrowid

def select_all_foods(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM foods")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

def main():
    foodDict = {}
    sql_create_foods_table = """ CREATE TABLE IF NOT EXISTS foods (
                                        title text NOT NULL,
                                        expiry_date text NOT NULL
                                    ); """

    database = "test.db"

    conn = create_connection(database)

    print("Successfully opened test.db")

    if conn is not None:
        create_table(conn, sql_create_foods_table)
        print("made foods tables")
    else:
        print("ERRORRRRRRRRRRRRRRRRR")

    with open('database.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} works in the {row[1]} department.')
                foodDict[row[0]] = row[1];
                line_count += 1
        print(f'Processed {line_count} lines.')
        print (foodDict)

    while True:
        found = False
        capture_image()
        objects = localize_objects('test.jpg')
        for object_ in objects:
            print('\n{} (confidence: {})'.format(object_.name, object_.score))
            print('Normalized bounding polygon vertices: ')
            for vertex in object_.bounding_poly.normalized_vertices:
                print(' - ({}, {})'.format(vertex.x, vertex.y))
            if object_.name.lower() in foodDict:
                print("Found "+object_.name+" which is in foodDict")
                expiry_date = foodDict.get(object_.name.lower())
                with conn:
                    food = (object_.name, expiry_date)
                    food_id = create_food(conn, food)
                    print("Successfully added "+object_.name+" to the SQLITe Database")
                found = True;
                break
        if found:
            print("2. Query all tasks")
            select_all_foods(conn)
            sleep(5)
            
        
    
        #sleep(0.5)

main()