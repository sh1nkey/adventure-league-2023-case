# Generated by Django 4.2.7 on 2023-11-08 14:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_alter_user_role_group_baseprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="students",
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
