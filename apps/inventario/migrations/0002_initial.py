# Generated by Django 3.2.13 on 2022-07-12 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proveedor_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='modeloitem',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modelo_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='modeloitem',
            name='marca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.marca'),
        ),
        migrations.AddField(
            model_name='marca',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marca_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventario_item',
            name='ModeloItem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventario_item_modelo', to='inventario.modeloitem'),
        ),
        migrations.AddField(
            model_name='inventario_item',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventario_item_categoria', to='inventario.categoria'),
        ),
        migrations.AddField(
            model_name='inventario_item',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventario_item_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventario_item',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventario_item_estado', to='inventario.estado'),
        ),
        migrations.AddField(
            model_name='inventario_item',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventario_item_proveedor', to='inventario.proveedor'),
        ),
        migrations.AddField(
            model_name='historial_asignacion',
            name='assigned_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignado_por', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historial_asignacion',
            name='assigned_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignado_a', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historial_asignacion',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creado_por', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historial_asignacion',
            name='inventario_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articulo', to='inventario.inventario_item'),
        ),
        migrations.AddField(
            model_name='estado',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estado_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='categoria',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
