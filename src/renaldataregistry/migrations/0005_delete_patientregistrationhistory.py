from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("renaldataregistry", "0004_patientregistrationhistory"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PatientRegistrationHistory",
        ),
    ]
