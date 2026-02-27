from django.apps import AppConfig

class TecwebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tecweb'

    def ready(self):
        # Repõe/cria o registo do django.contrib.sites para o admin não rebentar
        try:
            from django.conf import settings
            from django.contrib.sites.models import Site
            from django.db.utils import OperationalError, ProgrammingError

            site_id = getattr(settings, "SITE_ID", 1)
            domain = getattr(settings, "DEFAULT_DOMAIN", "tecweb26.pw.deisi.ulusofona.pt")
            site_name = getattr(settings, "DEFAULT_SITE_NAME", "tecweb26")

            Site.objects.update_or_create(
                id=site_id,
                defaults={"domain": domain, "name": site_name},
            )

        except (OperationalError, ProgrammingError):
            # BD ainda não está pronta (migrations)
            pass
        except Exception:
            # Não deixa a app falhar no arranque
            pass