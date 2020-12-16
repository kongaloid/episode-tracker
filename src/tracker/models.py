import os

from django.conf import settings
from django.db import models


class Show(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    poster_path = models.CharField(max_length=300, null=True, blank=True)
    next_episode_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    episode_number = models.IntegerField(null=True, blank=True)
    season_number = models.IntegerField(null=True, blank=True)
    episode_name = models.CharField(max_length=200, null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.name)

    def delete(self, *args, **kwargs):
        ''' delete image files when show is removed '''
        if self.poster_path:
            image = f'{settings.POSTER_PATH}{self.poster_path}'
            if os.path.exists(image):
                os.remove(image)
        super().delete(*args, **kwargs)
