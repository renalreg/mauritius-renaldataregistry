# Generated by Django 3.2.6 on 2022-02-17 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("renaldataregistry", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="pid",
            field=models.CharField(
                max_length=14, unique=True, verbose_name="Unique ID"
            ),
        ),
    ]