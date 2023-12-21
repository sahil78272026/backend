# Generated by Django 4.2.1 on 2023-10-12 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_singer_alter_generatedpdf_pdf_file_song"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sale",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sold_at", models.DateTimeField(auto_now_add=True)),
                ("charged_amount", models.PositiveIntegerField()),
            ],
        ),
    ]