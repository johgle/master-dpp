"""
Django views for the product app.
This file contains the logic for handling requests and rendering templates.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""


from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from product import dpp_agent, kb_client
from product import qr_generator
from datetime import datetime

def product_view(request):
    """Load the product page based on the DPP_ID."""
    
    dpp_id = request.GET.get('id', '').strip()  # Extract DPP_ID from the URL

    # Fetch data from the knowledge base using DPP_ID
    dpp_data = kb_client.get_dpp_data(dpp_id)
    if not dpp_data:
        return HttpResponse(f"No data found for DPP ID: {dpp_id}", status=404)

    # Calculate unique materials, total mass, and total volume
    parts = dpp_data["parts"]
    unique_materials = set(part["partMaterial"] for part in parts)
    total_mass = round(sum(part["partMass"] for part in parts), 2)  # Rounded to 2 decimals
    total_volume = round(sum(part["partVolume"] for part in parts), 2)  # Rounded to 2 decimals

    return render(request, 'product/product.html', {
        'dpp_id': dpp_id,
        'product': dpp_data["describes"],
        'actor': dpp_data["responsibleActor"],
        'timeStampInvalid': dpp_data["timeStampInvalid"],
        'allPartIDs': dpp_data["allParts"],
        'parts': parts,
        'unique_materials': ", ".join(unique_materials),
        'total_mass': total_mass,
        'total_volume': total_volume,
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
        did = request.POST.get('did', '').strip()
        wid = request.POST.get('wid', '').strip()
        eid = request.POST.get('eid', '').strip()

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
            if success_create and success_added_to_kb:
                ip_address = '172.20.10.3'  # Replace with your actual IP address
                qr_code_path = qr_generator.generate_qr_code(ip_address, dpp.id)  # Use DPP_ID
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

@csrf_exempt
def delete_dpp_view(request):
    """Handle the deletion of a Digital Product Passport."""
    success_delete = False
    error_message = None

    if request.method == 'POST':
        dpp_id = request.POST.get('dpp_id', '').strip()

        if not dpp_id:
            error_message = "DPP ID cannot be empty. Please provide a valid ID."
        else:
            try:
                # Fetch DPP data from the knowledge base
                dpp_data = kb_client.get_dpp_data(dpp_id)

                if not dpp_data:
                    error_message = f"No Digital Product Passport found with ID: {dpp_id}"
                else:
                    # Extract product and part IDs
                    product_id = dpp_data["describes"]["productID"]
                    all_part_ids = dpp_data["allParts"]

                    # Remove the DPP and associated product from the knowledge base
                    kb_client.update_kb(kb_client.make_remove_dpp_query(dpp_id))
                    kb_client.update_kb(kb_client.make_remove_product_query(product_id, all_part_ids))
                    success_delete = True
            except Exception as e:
                error_message = f"Error deleting the Digital Product Passport: {e}"

    return render(request, 'product/delete_dpp.html', {
        'success_delete': success_delete,
        'error_message': error_message,
    })

@csrf_exempt
def update_dpp_view(request):
    """Handle updating the timeStampInvalid and responsibleActor of a DPP."""
    success_update = False
    error_message = None
    dpp_data = None
    actor = None
    timestampinvalid = None

    if request.method == 'POST':
        dpp_id = request.POST.get('dpp_id', '').strip()
        new_timestamp_invalid = request.POST.get('timeStampInvalid', '').strip()
        new_actor_id = request.POST.get('actor_id', '').strip()

        if not dpp_id:
            error_message = "DPP ID cannot be empty. Please provide a valid ID."
        else:
            try:
                # Fetch the existing DPP data
                dpp_data = kb_client.get_dpp_data(dpp_id)
                if not dpp_data:
                    error_message = f"No Digital Product Passport found with ID: {dpp_id}"
                    print("DPP data ikke funnet",error_message)
                else:
                # Validate the timestamp format
                    if new_timestamp_invalid:
                        try:
                            datetime.strptime(new_timestamp_invalid, "%Y-%m-%d")
                        except ValueError:
                            error_message = "New timestamp must be in the format YYYY-MM-DD."
                            raise ValueError(error_message)

                    # Check if the actor ID exists in the database
                    if new_actor_id:
                        actor_data = kb_client.get_actor_data(new_actor_id)
                        if not actor_data:
                            error_message = f"No Actor found with ID: {new_actor_id}."
                            raise ValueError(error_message)

                    
                    # Update the timeStampInvalid and responsibleActor in the knowledge base
                    if not new_timestamp_invalid and not new_actor_id:
                        error_mesage = "A valid DPP ID was found, but no new timestamp or actor ID was provided." \
                                        "Please enter the new data you would like to use to update the passport."
                        raise ValueError(error_mesage)
                    if new_timestamp_invalid:
                        kb_client.update_kb(kb_client.make_update_timestamp_query(dpp_id, new_timestamp_invalid))
                    if new_actor_id:
                        kb_client.update_kb(kb_client.make_update_actor_query(dpp_id, new_actor_id))
                    success_update = True

                    # Fetch updated DPP data for confirmation
                    dpp_data = kb_client.get_dpp_data(dpp_id)
                    actor = dpp_data["responsibleActor"]
                    timestampinvalid = dpp_data["timeStampInvalid"]
            except Exception as e:
                if not error_message:  # To catch unexpected errors
                    error_message = f"Error updating the Digital Product Passport: {e}"
    return render(request, 'product/update_dpp.html', {
        'success_update': success_update,
        'error_message': error_message,
        'actor': actor,
        'timestampinvalid': timestampinvalid,
    })

