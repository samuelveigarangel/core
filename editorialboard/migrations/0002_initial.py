# Generated by Django 4.2.7 on 2023-12-14 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("researcher", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("editorialboard", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="editorialboardmember",
            name="researcher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="researcher.researcher",
            ),
        ),
        migrations.AddField(
            model_name="editorialboardmember",
            name="role",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="editorialboard.rolemodel",
            ),
        ),
        migrations.AddField(
            model_name="editorialboardmember",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_last_mod_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Updater",
            ),
        ),
        migrations.AddField(
            model_name="editorialboard",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Creator",
            ),
        ),
    ]