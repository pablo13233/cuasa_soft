# Generated by Django 3.2.13 on 2022-06-01 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='img_ticket',
            field=models.ImageField(default='img_defecto.jpg', upload_to='tickets/{User.username}/', verbose_name='Image'),
        ),
    ]
