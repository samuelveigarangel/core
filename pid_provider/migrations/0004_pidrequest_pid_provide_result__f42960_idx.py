# Generated by Django 4.1.10 on 2023-09-05 18:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pid_provider", "0003_remove_xmlrelateditem_creator_and_more"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="pidrequest",
            index=models.Index(
                fields=["result_type"], name="pid_provide_result__f42960_idx"
            ),
        ),
    ]
