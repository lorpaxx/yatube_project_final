# Generated by Django 2.2.9 on 2021-10-11 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20211011_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.CharField(max_length=200),
        ),
    ]
