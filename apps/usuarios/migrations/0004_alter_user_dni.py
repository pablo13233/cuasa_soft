# Generated by Django 3.2.13 on 2022-10-11 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_user_dni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dni',
            field=models.CharField(max_length=13),
        ),
    ]
