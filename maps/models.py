from django.db import models

class Map(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    data = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.pk}: {self.name}'
