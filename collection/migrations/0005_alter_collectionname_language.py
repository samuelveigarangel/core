# Generated by Django 4.1.8 on 2023-05-23 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_alter_license_options_rename_license_license_url_and_more"),
        (
            "collection",
            "0004_remove_collection_collection__type_fi_ccf430_idx_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="collectionname",
            name="language",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.language",
                verbose_name="Idioma",
            ),
        ),
    ]