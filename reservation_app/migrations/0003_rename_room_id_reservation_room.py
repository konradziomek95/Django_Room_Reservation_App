# Generated by Django 4.0.5 on 2022-06-19 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_app', '0002_reservation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='room_id',
            new_name='room',
        ),
    ]
