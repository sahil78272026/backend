# Generated by Django 4.2.2 on 2023-10-24 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_student_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='singer',
            table='singer',
        ),
        migrations.AlterModelTable(
            name='song',
            table='song',
        ),
    ]
