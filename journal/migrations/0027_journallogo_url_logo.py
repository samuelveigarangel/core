# Generated by Django 5.0.3 on 2024-08-04 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0026_editorialpolicy_opensciencecompliance"),
    ]

    operations = [
        migrations.AddField(
            model_name="journallogo",
            name="url_logo",
            field=models.URLField(blank=True, null=True),
        ),
    ]
