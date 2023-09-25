# import from django
from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=50)
    roll = models.IntegerField()
    city = models.CharField(max_length=50)


class Cloth(models.Model):
    item_id = models.IntegerField(primary_key=True)
    brand_name = models.CharField(max_length=20)
    fabric = models.CharField(max_length=20)
    sku = models.CharField(max_length=40)
    fitting_type = models.CharField(max_length=20)
    imported = models.BooleanField()
    category_id = models.CharField(max_length=10)



