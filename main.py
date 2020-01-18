# hard hack

import io
import os

import cv2
from time import sleep
from time import time

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
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))

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
        if elasped > 5:
            break
    cv2.imwrite(filename='test.jpg', img=frame)
    webcam.release()
    cv2.destroyAllWindows()
    print("Processing image...")

def main():
    capture_image()
    localize_objects('test.jpg')

main()