# Generated by Django 4.2.13 on 2024-06-24 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipments',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='equipments',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='equipments',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='equipments',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to='employees.employee'),
        ),
    ]
