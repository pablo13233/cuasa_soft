# Generated by Django 3.2.13 on 2022-08-30 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='control_Asignaciones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creado_por', to=settings.AUTH_USER_MODEL)),
                ('update_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actualizado_por', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='asignado_a', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='historial_asignaciones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('observaciones', models.TextField(blank=True, default='', max_length=500, null=True)),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asigna', to=settings.AUTH_USER_MODEL)),
                ('control_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asignaciones.control_asignaciones')),
                ('inventario_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.inventario_item')),
                ('update_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actualiza', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
