# Generated by Django 4.2.7 on 2023-12-13 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("editorialboard", "0005_alter_editorialboardrole_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="editorialboardrole",
            name="members",
        ),
        migrations.AddField(
            model_name="editorialboardrole",
            name="members",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="editorialboard.editorialboardmember",
            ),
        ),
    ]
