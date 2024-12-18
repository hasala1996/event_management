# Generated by Django 4.1.4 on 2024-11-15 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("security", "0003_remove_user_data_joined"),
    ]

    operations = [
        migrations.AddField(
            model_name="rol",
            name="permissions",
            field=models.ManyToManyField(
                blank=True, related_name="roles", to="auth.permission"
            ),
        ),
    ]
