import qrcode
import os
from django.conf import settings

def generate_qr_code_file(url, filename):
    """
    Generates a QR code for 'url' and saves it as 'filename'.
    """
    img = qrcode.make(url)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)


def get_local_ip_address():
    """
    Gets local IP-adress.
    """
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("1.1.1.1", 1))
        ip_adress = s.getsockname()[0]
    except Exception:
        ip_adress = "127.0.0.1"
    finally:
        s.close()
    return ip_adress