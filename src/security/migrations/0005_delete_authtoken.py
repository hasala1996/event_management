# Generated by Django 4.1.4 on 2024-11-15 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("security", "0004_rol_permissions"),
    ]

    operations = [
        migrations.DeleteModel(name="AuthToken",),
    ]
