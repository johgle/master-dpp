"""
Django views for the product app.
This file contains the logic for handling requests and rendering templates.
"""


from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def product_view(request):
    """dette er det som lastes inn på nettsiden"""
    # product_id = request.GET.get('id')  # Henter ?id=xxx fra URL-en
    # if product_id == 'stol_123':
    #     # Returner litt HTML-streng
    #     return HttpResponse("""
    #         <html>
    #           <body>
    #             <h1>Her er informasjon om stol_123 (Django-versjon)</h1>
    #             <p>Dette er en spesiell stol.Her er et bilde:</p>
    #             <img src="/static/qr_code.png" alt="Stol 123" style="max-width: 300px;">
    #           </body>
    #         </html>
    #     """)
    # else:
    #     return HttpResponse(f"<h1>Produkt: {product_id} (Django-versjon)</h1>")

    product_id = request.GET.get('id', '')
    return render(request, 'product/product.html', {
        'product_id': product_id,
    })

