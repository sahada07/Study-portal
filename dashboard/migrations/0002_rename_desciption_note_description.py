# Generated by Django 5.2 on 2025-04-22 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='desciption',
            new_name='description',
        ),
    ]
