# Generated by Django 4.2.7 on 2023-12-29 15:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("collection", "0001_initial"),
        ("pid_provider", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="collectionpidrequest",
            unique_together={("collection",)},
        ),
    ]