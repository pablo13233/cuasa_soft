# Generated by Django 3.2.13 on 2022-06-10 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_alter_ticket_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='assignee',
            new_name='assignee_id',
        ),
    ]