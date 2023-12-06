# Generated by Django 4.2.7 on 2023-12-06 01:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import report.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("journal", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReportCSV",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Creation date"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last update date"
                    ),
                ),
                (
                    "title",
                    models.TextField(
                        blank=True,
                        help_text="Complete with the type of report",
                        null=True,
                        verbose_name="Title",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=report.models.csv_directory_path,
                        verbose_name="File",
                    ),
                ),
                (
                    "columns",
                    models.JSONField(blank=True, null=True, verbose_name="JSON File"),
                ),
                (
                    "publication_year",
                    models.CharField(
                        blank=True,
                        max_length=4,
                        null=True,
                        verbose_name="Publication Year",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Creator",
                    ),
                ),
                (
                    "journal",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="journal.journal",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_last_mod_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updater",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
