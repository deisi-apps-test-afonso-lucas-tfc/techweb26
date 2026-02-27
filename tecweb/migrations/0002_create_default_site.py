

from django.db import migrations


def create_site(apps, schema_editor):
    Site = apps.get_model("sites", "Site")

    # Ajusta domínio/nome se quiseres, mas assim já resolve o admin
    Site.objects.update_or_create(
        id=1,
        defaults={"domain": "tecweb26.pw.deisi.ulusofona.pt", "name": "tecweb26"},
    )


class Migration(migrations.Migration):

    dependencies = [
        ("tecweb", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_site, migrations.RunPython.noop),
    ]