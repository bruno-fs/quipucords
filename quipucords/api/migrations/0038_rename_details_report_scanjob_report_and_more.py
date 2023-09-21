# Generated by Django 4.2.4 on 2023-09-21 15:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0037_rename_detailsreport_report"),
    ]

    operations = [
        migrations.RenameField(
            model_name="scanjob",
            old_name="details_report",
            new_name="report",
        ),
        migrations.AlterField(
            model_name="report",
            name="deployment_report",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="report",
                to="api.deploymentsreport",
            ),
        ),
    ]
