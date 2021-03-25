from django.db import models

class Map(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    coordinates = models.JSONField(default=dict)
    data = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.pk}: {self.coordinates}'
