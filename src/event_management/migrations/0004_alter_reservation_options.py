# Generated by Django 4.1.4 on 2024-11-15 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("event_management", "0003_alter_event_options_alter_reservation_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="reservation", options={"ordering": ["reservation_date"]},
        ),
    ]
