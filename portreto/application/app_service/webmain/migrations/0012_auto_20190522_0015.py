# Generated by Django 2.2.1 on 2019-05-22 00:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webmain', '0011_auto_20190521_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='GalleryOwner',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
