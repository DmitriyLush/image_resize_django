from django.db import models


class Images(models.Model):
    url = models.CharField(blank=True, max_length=15000)
    file = models.FileField(blank=True, default=None, upload_to='images')


    class Meta:
        db_table = "images"