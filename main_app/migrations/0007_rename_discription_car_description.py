# Generated by Django 3.2 on 2021-04-22 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='discription',
            new_name='description',
        ),
    ]
