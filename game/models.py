from django.db import models

# Create your models here.
class Owner(models.Model):
    name = models.CharField(max_length=100)


class Company(models.Model):
    asset = models.CharField(max_length=150)
    investment = models.PositiveSmallIntegerField()
    coefficient = models.PositiveSmallIntegerField()
    share = models.ForeignKey('Share', related_name='companies', on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(Owner, related_name='companies', on_delete=models.CASCADE)


class Share(models.Model):
    color = models.CharField(max_length=20)