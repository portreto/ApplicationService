# Generated by Django 2.2.1 on 2019-05-19 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webmain', '0007_auto_20190518_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='FirstName',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='LastName',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]