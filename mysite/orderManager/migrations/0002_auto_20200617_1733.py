# Generated by Django 3.0.6 on 2020-06-17 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderManager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='table',
            new_name='customer',
        ),
    ]
