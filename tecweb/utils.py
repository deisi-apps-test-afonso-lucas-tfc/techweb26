# utils.py (ou no próprio views.py)
import subprocess
import tempfile
from datetime import date
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import date
import threading

ULTIMO_DIA_ENVIO = None

def enviar_backup_se_necessario():
    
    global ULTIMO_DIA_ENVIO
    hoje = date.today()
    if ULTIMO_DIA_ENVIO == hoje:
        return

    ULTIMO_DIA_ENVIO = hoje

    def faz_backup():
        # criar ficheiro temporário
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            backup_file = tmp.name

        # dump da base de dados
        subprocess.run([
            "python",
            "manage.py",
            "dumpdata",
            "--natural-foreign",
            "--natural-primary",
            "--indent", "2",
        ], stdout=open(backup_file, "w"))

        # email
        email = EmailMessage(
            subject="TecWeb 2026 – Backup diário da base de dados",
            body="Backup automático diário da plataforma TecWeb.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=["lucio.studer@ulusofona.pt"],
        )

        email.attach_file(backup_file)
        email.send(fail_silently=True)
    
    threading.Thread(target=faz_backup, daemon=True).start()