from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    year = models.IntegerField(null=True, blank=True)
    design = models.CharField(max_length=100, blank=True)
    

    # Felt for å lagre QR-koden som et bilde
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        return self.name
