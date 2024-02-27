from django.db import migrations, models


def tie_sys_inspection_result_to_scanjob(apps, schema_editor):
    """Bind SystemInspectionResult to ScanJob skipping intermediary models."""
    SystemInspectionResult = apps.get_model("api", "SystemInspectionResult")
    M2MModel = SystemInspectionResult.scanjobs.through
    m2m_instances = []
    for result in SystemInspectionResult.objects.prefetch_related(
        "task_inspection_result__job_inspection_result__scanjob"
    ).all():
        scanjob_id = result.task_inspection_result.job_inspection_result.scanjob.id
        m2m_instances.append(
            M2MModel(systeminspectionresult_id=result.id, scanjob_id=scanjob_id)
        )
    M2MModel.objects.bulk_create(m2m_instances)


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0045_merge_source_options_with_source"),
    ]

    operations = [
        migrations.AddField(
            model_name="systeminspectionresult",
            name="scanjobs",
            field=models.ManyToManyField(to="api.scanjob"),
        ),
        migrations.RunPython(
            tie_sys_inspection_result_to_scanjob, reverse_code=migrations.RunPython.noop
        ),
    ]
