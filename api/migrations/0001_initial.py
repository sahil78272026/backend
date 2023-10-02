# Generated by Django 4.2.2 on 2023-09-26 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cloth',
            fields=[
                ('item_id', models.IntegerField(primary_key=True, serialize=False)),
                ('brand_name', models.CharField(max_length=20)),
                ('fabric', models.CharField(max_length=20)),
                ('sku', models.CharField(max_length=40)),
                ('fitting_type', models.CharField(max_length=20)),
                ('imported', models.BooleanField()),
                ('category_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('roll', models.IntegerField()),
                ('city', models.CharField(max_length=50)),
            ],
        ),
    ]
