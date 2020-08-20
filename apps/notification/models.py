from django.db import models


class CustomContentType(models.Model):
    type = models.CharField(max_length=10)
    description = models.CharField(max_length=50)

    def __str__(self):
        return f'Content type: {self.type}'
