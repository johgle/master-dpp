# # product/signals.py
# import os
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings

# from .models import Product
# from .utils import generate_qr_code_file

# @receiver(post_save, sender=Product)
# def post_save_generate_qr(sender, instance, created, **kwargs):
#     """
#     Når et nytt Product-objekt er opprettet, generes en QR-kode.
#     """
#     if created:
#         # Bygg en URL som peker til produktets side i Django
#         # (Her bruker vi IP + port du allerede har i ALLOWED_HOSTS)
#         # I praksis bør du kanskje bygge URL dynamisk (settings.py, request osv.)
#         product_url = f"http://192.168.10.181:8000/product?id={instance.name}" #fra .pk til .name

#         # Definer filnavn inne i MEDIA_ROOT, f.eks:
#         qr_filename = os.path.join(
#             settings.MEDIA_ROOT,
#             'qrcodes',
#             f"product_{instance.name}.png"
#         )

#         # Generer og lagre filen
#         generate_qr_code_file(product_url, qr_filename)

#         # Oppdater 'qr_code'-feltet til å peke på 'qrcodes/product_<id>.png'
#         instance.qr_code = f"qrcodes/product_{instance.name}.png"
#         # For å unngå re-kjøring av signals, kall save() med update_fields
#         instance.save(update_fields=['qr_code'])
