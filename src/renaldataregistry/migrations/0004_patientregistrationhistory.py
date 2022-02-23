from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("renaldataregistry", "0003_alter_patientmeasurement_measurementtype"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patientakimeasurement",
            name="creatinine",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=6,
                null=True,
                verbose_name="Latest creatinine (μmol/l)",
            ),
        ),
        migrations.AlterField(
            model_name="patientakimeasurement",
            name="egfr",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=5,
                null=True,
                verbose_name="Latest eGFR (ml/min)",
            ),
        ),
        migrations.CreateModel(
            name="PatientRegistrationHistory",
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
                ("action", models.CharField(max_length=6)),
                ("action_tstamp", models.DateTimeField(auto_now=True)),
                (
                    "action_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="prh_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "new_health_institution",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="new_health_institution",
                        to="renaldataregistry.healthinstitution",
                        verbose_name="New health institution",
                    ),
                ),
                (
                    "new_unit",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="new_unit",
                        to="renaldataregistry.unit",
                        verbose_name="New unit",
                    ),
                ),
                (
                    "original_health_institution",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="original_health_institution",
                        to="renaldataregistry.healthinstitution",
                        verbose_name="Original health institution",
                    ),
                ),
                (
                    "original_unit",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="original_unit",
                        to="renaldataregistry.unit",
                        verbose_name="Original unit",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="renaldataregistry.patient",
                        verbose_name="Patient",
                    ),
                ),
            ],
        ),
    ]
