# Generated by Django 4.2.1 on 2024-01-07 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_fueltype_carmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='fueltype',
            field=models.ManyToManyField(blank=True, null=True, to='api.fueltype'),
        ),
        migrations.AlterField(
            model_name='carmodel',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='fueltype',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]