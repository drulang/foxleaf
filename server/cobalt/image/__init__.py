import os

from django.conf import settings

from cobalt import models

print("CWD: %s" % os.getcwd())

PROFILE_IMAGE_PATH = os.path.join(settings.BASE_DIR, 'profileimages')
ART_IMAGE_PATH = os.path.join(settings.BASE_DIR, 'artimages')

PROFILE_IMAGE_TYPE = models.ImageType.objects.filter(imagetypcd="prfle").first()
ART_IMAGE_TYPE = models.ImageType.objects.filter(imagetypcd="art").first()

SUPPORTED_IMAGE_TYPES = [
    "image/jpeg",
    "image/png",
]

MAX_FILE_SIZE = 30000000 # ~30MB

if not os.path.exists(PROFILE_IMAGE_PATH):
    try:
        os.makedirs(PROFILE_IMAGE_PATH)
    except Exception as e:
        print("Unable to create directory. Err: %s" % e)

if not os.path.exists(ART_IMAGE_PATH):
    try:
        os.makedirs(ART_IMAGE_PATH)
    except Exception as e:
        print("Unable to create directory. Err: %s" % e)

def image_type_valid(content_type):
    return content_type in SUPPORTED_IMAGE_TYPES

def handle_uploaded_image(filedata, filename):
    with open(filename, 'wb+') as destination:
        for chunk in filedata.chunks():
            destination.write(chunk)
