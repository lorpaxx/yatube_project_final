# Generated by Django 2.2.9 on 2021-10-11 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20211011_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(),
        ),
    ]
