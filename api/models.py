# import from django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator
from multiselectfield import MultiSelectField


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

class NewUser(models.Model):
    name  = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)


class Student(models.Model):
    name = models.CharField(max_length=50)
    roll = models.IntegerField()
    city = models.CharField(max_length=50)
    order_id = models.CharField(max_length=50, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    datetime_of_payment = models.DateField(auto_now_add=True, null=True, blank=True)
    total_amount = models.DecimalField(max_length=50, decimal_places=2, max_digits=4, null=True, blank=True)
    invoice = models.FileField(upload_to="invoice/", null=True, blank=True)


    # teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


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




