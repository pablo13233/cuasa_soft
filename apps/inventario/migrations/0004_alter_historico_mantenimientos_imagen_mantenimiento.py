# Generated by Django 3.2.13 on 2023-05-25 07:24

import apps.inventario.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_historico_mantenimientos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historico_mantenimientos',
            name='imagen_mantenimiento',
            field=models.ImageField(default='img_defecto.jpg', upload_to=apps.inventario.models.get_item_image_folder_maintenance, verbose_name='Image_Maintenance'),
        ),
    ]
