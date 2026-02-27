from django.db import migrations

def fix_site_domain(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    
    site, created = Site.objects.get_or_create(id=1)
    site.domain = 'tecweb26.pw.deisi.ulusofona.pt'
    site.name = 'Tecweb 2026'
    site.save()

class Migration(migrations.Migration):
    dependencies = [
        ('tecweb', '0001_initial'), 
    ]
    operations = [
        migrations.RunPython(fix_site_domain),
    ]