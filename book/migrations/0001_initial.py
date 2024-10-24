# Generated by Django 4.1.6 on 2023-03-06 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("location", "0004_alter_state_name"),
        ("institution", "0003_alter_institution_acronym_and_more"),
        ("core", "0002_language"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("researcher", "0004_alter_researcher_creator_alter_researcher_updated_by"),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
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
                    models.CharField(
                        blank=True, max_length=256, null=True, verbose_name="Título"
                    ),
                ),
                (
                    "synopsis",
                    models.TextField(blank=True, null=True, verbose_name="Synopsis"),
                ),
                (
                    "isbn",
                    models.CharField(
                        blank=True, max_length=13, null=True, verbose_name="ISBN"
                    ),
                ),
                (
                    "eisbn",
                    models.CharField(
                        blank=True,
                        max_length=13,
                        null=True,
                        verbose_name="Electronic ISBN",
                    ),
                ),
                (
                    "doi",
                    models.CharField(
                        blank=True, max_length=256, null=True, verbose_name="DOI"
                    ),
                ),
                (
                    "year",
                    models.IntegerField(blank=True, null=True, verbose_name="Year"),
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
                    "institution",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="institution.institution",
                        verbose_name="Publisher",
                    ),
                ),
                (
                    "language",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.language",
                        verbose_name="Idioma",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="location.location",
                        verbose_name="Localization",
                    ),
                ),
                (
                    "researchers",
                    models.ManyToManyField(
                        blank=True, to="researcher.researcher", verbose_name="Authors"
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
                "verbose_name": "SciELO Book",
                "verbose_name_plural": "SciELO Books",
            },
        ),
        migrations.CreateModel(
            name="Chapter",
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
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
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
                    models.CharField(
                        blank=True, max_length=256, null=True, verbose_name="Título"
                    ),
                ),
                (
                    "publication_date",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Data de publicação",
                    ),
                ),
                (
                    "book",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chapter",
                        to="book.book",
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
                    "language",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.language",
                        verbose_name="Idioma",
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
                "verbose_name": "Chapter",
                "verbose_name_plural": "Chapters",
            },
        ),
        migrations.AddIndex(
            model_name="chapter",
            index=models.Index(fields=["title"], name="book_chapte_title_5891b0_idx"),
        ),
        migrations.AddIndex(
            model_name="chapter",
            index=models.Index(
                fields=["language"], name="book_chapte_languag_3589ab_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="chapter",
            index=models.Index(
                fields=["publication_date"], name="book_chapte_publica_262182_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="book",
            index=models.Index(fields=["isbn"], name="book_book_isbn_6f139e_idx"),
        ),
        migrations.AddIndex(
            model_name="book",
            index=models.Index(fields=["title"], name="book_book_title_b5b75a_idx"),
        ),
        migrations.AddIndex(
            model_name="book",
            index=models.Index(
                fields=["synopsis"], name="book_book_synopsi_3faa60_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="book",
            index=models.Index(fields=["doi"], name="book_book_doi_3c6aea_idx"),
        ),
    ]
