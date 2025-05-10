"""
Django views for the product app.
This file contains the logic for handling requests and rendering templates.
"""


from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from product import dpp_agent

# Create your views here.

def product_view(request):
    """dette er det som lastes inn på nettsiden"""
    
    product_id = request.GET.get('id', '')

    # Extract DID, WID, and EID from the product_id
    did, wid, eid = ('', '', '')
    if product_id:
        try:
            did, wid, eid = product_id.split('_')
        except ValueError:
            pass  # Handle cases where the ID format is incorrect

    return render(request, 'product/product.html', {
        'product_id': product_id,
        'did': did,
        'wid': wid,
        'eid': eid,
    })

@csrf_exempt
def new_dpp_view(request):
    success = False
    part_ids = []
    error_message = None

    if request.method == 'POST':
        did = request.POST.get('did', '')
        wid = request.POST.get('wid', '')
        eid = request.POST.get('eid', '')

        # Call make_part_instance and retrieve part IDs
        try:
            parts = dpp_agent.make_part_instance(did, wid, eid)
            part_ids = [part.id for part in parts]
            success = True
        except Exception as e:
            error_message = f"Error creating parts: {e}"

    return render(request, 'product/new_dpp.html', {
        'success': success,
        'part_ids': part_ids,
        'error_message': error_message,
    })

