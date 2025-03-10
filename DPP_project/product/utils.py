import qrcode
import os
from django.conf import settings

def generate_qr_code_file(url, filename):
    """
    Lager en QR-kode for 'url' og lagrer den som 'filename'.
    """
    img = qrcode.make(url)
    # Sørg for at katalogen finnes
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)
