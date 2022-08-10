# Generated by Django 2.2.4 on 2019-12-16 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_systemfingerprint_virtual_host_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="deploymentsreport",
            name="cached_masked_csv",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="deploymentsreport",
            name="cached_masked_fingerprints",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="detailsreport",
            name="cached_masked_csv",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="systemfingerprint",
            name="cloud_provider",
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name="systemfingerprint",
            name="cpu_hyperthreading",
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name="systemfingerprint",
            name="system_purpose",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="systemfingerprint",
            name="system_user_count",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="systemfingerprint",
            name="user_login_history",
            field=models.TextField(null=True),
        ),
    ]
