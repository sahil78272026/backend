# Generated by Django 4.2.1 on 2024-01-29 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0022_delete_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="desc",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
