# Generated by Django 2.2.6 on 2019-12-05 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0005_auto_20191128_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='numberOfClicks',
            field=models.IntegerField(default=0),
        ),
    ]
