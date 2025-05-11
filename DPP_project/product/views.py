"""
Django views for the product app.
This file contains the logic for handling requests and rendering templates.
"""


from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from product import dpp_agent, kb_client
from product import qr_generator

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

    # her vet vi hva did, wid og eid er.
    # hente ut data fra KB gjennom dpp_agent

    return render(request, 'product/product.html', {
        'product_id': product_id,
        'did': did,
        'wid': wid,
        'eid': eid,
    })

@csrf_exempt
def new_dpp_view(request):
    success_create = False
    success_added_to_kb = False
    success_qr_code = False
    qr_code_path = None  # Initialize QR code path
    part_ids = []
    error_message = None
    dpp = None
    product = None
    actor = None

    if request.method == 'POST':
        did = request.POST.get('did', '')
        wid = request.POST.get('wid', '')
        eid = request.POST.get('eid', '')

        # Call make_part_instance and retrieve part IDs
        try:
            product, actor, dpp = dpp_agent.make_instances(did, wid, eid)
            success_create = True
        except Exception as e:
            error_message = f"Error creating product, actor or digital product passport: {e}"

        try:
            kb_client.update_kb(kb_client.make_insert_product_query(product))
            kb_client.update_kb(kb_client.make_insert_actor_query(actor))
            kb_client.update_kb(kb_client.make_insert_dpp_query(dpp))
            success_added_to_kb = True
        except Exception as e:
            error_message = f"Error adding product, actor or digital product passport to KB: {e}"
        
        try:
            ip_address = '10.22.120.185'  # Replace with your actual IP address
            qr_code_path = qr_generator.generate_qr_code(ip_address, did, wid, eid)
            if qr_code_path:
                success_qr_code = True
        except Exception as e:
            error_message = f"Error generating QR code: {e}"

    return render(request, 'product/new_dpp.html', {
        'success_create': success_create,
        'success_added_to_kb': success_added_to_kb,
        'success_qr_code': success_qr_code,
        'qr_code_path': qr_code_path,  # Pass the QR code path to the template
        'product': product,
        'part_ids': product.parts if product else [],
        'actor': actor,
        'dpp': dpp,
        'error_message': error_message,
    })

