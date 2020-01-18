# hard hack

import io
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="environ.json"

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

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

import cv2
from time import sleep
sleep(2)
webcam = cv2.VideoCapture(0)
check, frame = webcam.read()
cv2.imshow("Capturing", frame)
cv2.imwrite(filename='test.jpg', img=frame)
webcam.release()
print("Processing image...")

localize_objects('test.jpg')