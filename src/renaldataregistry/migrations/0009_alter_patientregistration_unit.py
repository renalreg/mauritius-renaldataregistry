# Generated by Django 3.2.6 on 2022-06-13 13:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("renaldataregistry", "0008_alter_patientkrtmodality_hd_tcntcreason"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="patientregistration",
            name="unit",
        ),
        migrations.AddField(
            model_name="historicalpatientregistration",
            name="unit_no1",
            field=models.CharField(
                blank=True,
                max_length=6,
                null=True,
                validators=[django.core.validators.RegexValidator("^\\d{1,10}$")],
                verbose_name="Unit number 1",
            ),
        ),
        migrations.AddField(
            model_name="historicalpatientregistration",
            name="unit_no2",
            field=models.CharField(
                blank=True,
                max_length=6,
                null=True,
                validators=[django.core.validators.RegexValidator("^\\d{1,10}$")],
                verbose_name="Unit number 2",
            ),
        ),
        migrations.AddField(
            model_name="historicalpatientregistration",
            name="unit_no3",
            field=models.CharField(
                blank=True,
                max_length=6,
                null=True,
                validators=[django.core.validators.RegexValidator("^\\d{1,10}$")],
                verbose_name="Unit number 3",
            ),
        ),
        migrations.AddField(
            model_name="patientregistration",
            name="unit_no1",
            field=models.CharField(
                blank=True,
                max_length=6,
                null=True,
                validators=[django.core.validators.RegexValidator("^\\d{1,10}$")],
                verbose_name="Unit number 1",
            ),
        ),
        migrations.AddField(
            model_name="patientregistration",
            name="unit_no2",
            field=models.CharField(
                blank=True,
                max_length=6,
                null=True,
                validators=[django.core.validators.RegexValidator("^\\d{1,10}$")],
                verbose_name="Unit number 2",
            ),
        ),
        migrations.AddField(
            model_name="patientregistration",
            name="unit_no3",
            field=models.CharField(
                blank=True,
                max_length=6,
                null=True,
                validators=[django.core.validators.RegexValidator("^\\d{1,10}$")],
                verbose_name="Unit number 3",
            ),
        ),
        migrations.DeleteModel(
            name="Unit",
        ),
    ]
