# Generated by Django 4.2.7 on 2023-12-13 18:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_gender_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="license",
            unique_together={("url", "license_type")},
        ),
    ]
