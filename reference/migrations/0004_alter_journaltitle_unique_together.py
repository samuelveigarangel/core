# Generated by Django 4.2.7 on 2024-02-27 19:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("journal", "0019_alter_journallogo_unique_together"),
        ("reference", "0003_alter_journaltitle_title"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="journaltitle",
            unique_together={("journal", "title")},
        ),
    ]