from django.db import models


class World(models.Model):

    name = models.CharField(max_length=100)


class Continent(models.Model):

    name = models.CharField(max_length=100)


class Nation(models.Model):

    name = models.CharField(max_length=100)
