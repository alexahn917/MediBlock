# coding: utf-8

import io
from enum import Enum

# Imports the Google Cloud client library
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

# Use credentials for google client
credentials = service_account.Credentials.from_service_account_file('credentials.json')
client = vision.ImageAnnotatorClient(credentials=credentials)

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def draw_boxes(image, type_bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    # [START draw_blocks]
    draw = ImageDraw.Draw(image)

    for feature, type_bound in type_bounds.items():
        for bound in type_bound:
            draw.polygon([
                bound.vertices[0].x, bound.vertices[0].y,
                bound.vertices[1].x, bound.vertices[1].y,
                bound.vertices[2].x, bound.vertices[2].y,
                bound.vertices[3].x, bound.vertices[3].y], None, color[feature])
    return image
    # [END draw_blocks]


def get_document_bounds(image_file, features):
    # [START detect_bounds]
    """Returns document bounds given an image."""

    type_bounds = {}
    for feature in features:
        type_bounds[feature] = []

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (FeatureType.SYMBOL in features):
                            type_bounds[FeatureType.SYMBOL].append(symbol.bounding_box)
                    if (FeatureType.WORD in features):
                        type_bounds[FeatureType.WORD].append(word.bounding_box)
                if (FeatureType.PARA in features):
                    type_bounds[FeatureType.PARA].append(paragraph.bounding_box)
            if (FeatureType.BLOCK in features):
                type_bounds[FeatureType.BLOCK].append(block.bounding_box)

        if (FeatureType.PAGE in features):
            type_bounds[FeatureType.PAGE].append(block.bounding_box)

    return document.text, type_bounds

def render_doc_text(filein, fileout):
    typeColors = {
        FeatureType.PAGE:'blue',
        FeatureType.PARA:'red',
        FeatureType.WORD:'yellow'
    }
    image = Image.open(filein)
    text, bounds = get_document_bounds(filein, typeColors)
    draw_boxes(image, bounds, typeColors)

    # if fileout is not 0:
    #     image.save(fileout)
    image.show()

render_doc_text('img/med2.jpg', 'img/test.jpg')

