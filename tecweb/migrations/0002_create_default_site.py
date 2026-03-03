from django.db import migrations
import os


def create_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    domain = os.environ.get('SITE_DOMAIN', 'tecweb26.pw.deisi.ulusofona.pt')
    name = os.environ.get('SITE_NAME', 'tecweb26')
    Site.objects.update_or_create(
        id=1,
        defaults={'domain': domain, 'name': name},
    )


def reverse_create_default_site(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('tecweb', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(create_default_site, reverse_create_default_site),
    ]
