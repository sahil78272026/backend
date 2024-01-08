# import from django
from django.contrib.auth.models import (AbstractBaseUser, AbstractUser,
                                        PermissionsMixin, User)
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

# class Teacher(models.Model):
#     name = models.CharField(max_length=50)

    # @classmethod
    # def get_default_pk(cls):
    #     teacher, created = cls.objects.get_or_create(
    #             title='default teacher',
    #             defaults=dict(description='this is not a teacher'),
    #         )
    #     return teacher.pk

# Create your models here

# implemented django signals post_save(), see signals.py file and apps.py file

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)

class NewUser(models.Model):
    name  = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,  null=True, blank=True)

class Student(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.IntegerField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    roll = models.IntegerField(null=True, blank=True)
    order_id = models.CharField(max_length=50, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    datetime_of_payment = models.DateField(auto_now_add=True, null=True, blank=True)
    total_amount = models.DecimalField(max_length=50, decimal_places=2, max_digits=4, null=True, blank=True)
    invoice = models.FileField(upload_to="invoice/", null=True, blank=True)


    # teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "student"



class Cloth(models.Model):
    item_id = models.IntegerField(primary_key=True)
    brand_name = models.CharField(max_length=20)
    fabric = models.CharField(max_length=20)
    sku = models.CharField(max_length=40)
    fitting_type = models.CharField(max_length=20)
    imported = models.BooleanField()
    category_id = models.CharField(max_length=10)

class GeneratedPDF(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    pdf_file = models.FileField(upload_to='invoice', null=True, blank=True)


# For Nested Serializer
class Singer(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'singer'

class Movie(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table='movie'

class Song(models.Model):
    title = models.CharField(max_length=100)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE, related_name='sungby', null=True, blank=True)
    duration = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie', null=True, blank=True)

    class Meta:
        db_table='song'

    def __str__(self):
        return self.title



class Sale(models.Model):
    sold_at = models.DateTimeField(
        auto_now_add=True,db_index=True,
    )
    charged_amount = models.PositiveIntegerField()


# models for Many-to-Many Relationship check
class FuelType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'fueltype'



class CarModel(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    fueltype = models.ManyToManyField(FuelType, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table='carmodel'


