# Generated by Django 4.2.2 on 2023-10-01 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_student_datetime_of_payment_student_email_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='NewUser',
        ),
    ]
