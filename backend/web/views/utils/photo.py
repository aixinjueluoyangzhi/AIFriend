import os

from django.conf import settings


def remove_old_photo(photo):
    if photo and photo.name != 'user/photos/default.png':
        old_photo = settings.MEDIA_ROOT / photo.name
        if os.path.exists(old_photo):
            os.remove(old_photo)