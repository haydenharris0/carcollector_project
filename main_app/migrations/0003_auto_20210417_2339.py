# Generated by Django 3.2 on 2021-04-17 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_washing'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='color',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AddField(
            model_name='car',
            name='discription',
            field=models.CharField(default='NA', max_length=50),
        ),
        migrations.AddField(
            model_name='car',
            name='nickname',
            field=models.CharField(default='no nickname', max_length=40),
        ),
        migrations.AlterField(
            model_name='car',
            name='make',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='car',
            name='model',
            field=models.CharField(default='NA', max_length=20),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.IntegerField(default=0),
        ),
    ]
