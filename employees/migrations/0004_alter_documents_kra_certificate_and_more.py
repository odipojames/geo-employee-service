# Generated by Django 4.2.13 on 2024-07-04 09:23

from django.db import migrations, models
import utils.storages
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_alter_documents_kra_certificate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='kra_certificate',
            field=models.FileField(storage=utils.storages.OverwriteStorage(), upload_to='documents/kra_certificate/', validators=[utils.validators.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='documents',
            name='national_id',
            field=models.FileField(storage=utils.storages.OverwriteStorage(), upload_to='documents/national_id/', validators=[utils.validators.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='documents',
            name='others',
            field=models.FileField(blank=True, storage=utils.storages.OverwriteStorage(), upload_to='documents/others/', validators=[utils.validators.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='documents',
            name='passport_photo',
            field=models.ImageField(storage=utils.storages.OverwriteStorage(), upload_to='documents/passport_photo/'),
        ),
    ]
