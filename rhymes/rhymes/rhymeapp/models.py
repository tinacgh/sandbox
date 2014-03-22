from django.db import models

# Create your models here.
class Word(models.Model):
    trad = models.CharField(max_length=20)
    entry = models.CharField(max_length=500)
    fullending = models.CharField(max_length=30)
    fuzzyending = models.CharField(max_length=30)
    def __str__(self):
        return self.trad

class Ending(models.Model):
    pinyin = models.CharField(max_length=8)
    modified = models.CharField(max_length=8)
    def __str__(self):
        return pinyin + ":" + modified