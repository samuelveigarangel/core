# Generated by Django 5.0.3 on 2024-03-22 14:00

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("vocabulary", "0002_alter_keyword_unique_together_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="keyword",
            name="html_text",
            field=wagtail.fields.RichTextField(
                blank=True, null=True, verbose_name="Rich Text"
            ),
        ),
    ]
