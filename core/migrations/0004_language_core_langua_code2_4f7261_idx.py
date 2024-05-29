# Generated by Django 5.0.3 on 2024-05-27 17:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_gender_created_gender_creator_gender_updated_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name="language",
            index=models.Index(fields=["code2"], name="core_langua_code2_4f7261_idx"),
        ),
    ]