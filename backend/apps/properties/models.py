from django.db import models

class Property(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    municipality = models.CharField(max_length=100)
    province = models.CharField(max_length=50)
    cadastral_sheet = models.CharField(max_length=20, blank=True)
    cadastral_particle = models.CharField(max_length=20, blank=True)
    cadastral_subaltern = models.CharField(max_length=20, blank=True)
    domus_score = models.IntegerField(default=0)

    def __str__(self):
        return self.title
