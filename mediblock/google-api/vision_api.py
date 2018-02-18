# coding: utf-8
import base64
import io
from enum import Enum
from google.cloud.vision import types
from PIL import Image, ImageDraw
from django.conf import settings

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def draw_boxes(image, type_bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    for feature, type_bound in type_bounds.items():
        for bound in type_bound:
            draw.polygon([
                bound.vertices[0].x, bound.vertices[0].y,
                bound.vertices[1].x, bound.vertices[1].y,
                bound.vertices[2].x, bound.vertices[2].y,
                bound.vertices[3].x, bound.vertices[3].y], None, color[feature])
    return image

def get_document_bounds(image_file, features):
    """Returns document bounds given an image."""

    type_bounds = {}
    for feature in features:
        type_bounds[feature] = []

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = settings.GOOGLE_CLIENT.document_text_detection(image=image)
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

def render_doc_text(base64str):
    typeColors = {
        FeatureType.PAGE:'blue',
        FeatureType.PARA:'red',
        FeatureType.WORD:'yellow'
    }
    fout = open('temp.jpg', 'wb')
    fout.write(base64.b64decode(base64str))
    fout.flush()
    image = Image.open('temp.jpg')
    text, bounds = get_document_bounds('temp.jpg', typeColors)
    draw_boxes(image, bounds, typeColors)
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str, text