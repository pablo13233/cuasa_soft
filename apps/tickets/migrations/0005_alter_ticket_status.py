# Generated by Django 3.2.13 on 2022-06-10 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_alter_ticket_img_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('Abierto', 'Open'), ('En progreso', 'In Progress'), ('Terminado', 'Done')], default='Abierto', max_length=25),
        ),
    ]