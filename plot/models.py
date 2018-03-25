from django.db import models


class Encounter(models.Model):
    question = models.CharField(max_length=255)


class Adventure(models.Model):
    pass
