"""
Generate QR code for DPP using DPP ID

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

import qrcode
import os

def generate_qr_code(ip_adress, DPP_ID):
    try:
        url = f"http://{ip_adress}:8000/product/?id={DPP_ID}"
        filename = f"{DPP_ID}_qrcode.png"

        # Define the relative path to the qrcodes folder (inside the media directory)
        qr_code_folder = os.path.join('media', 'qrcodes')
        full_path = os.path.join(qr_code_folder, filename)

        # Ensure the directory exists
        os.makedirs(qr_code_folder, exist_ok=True)

        # Generate and save the QR code image
        qr_code_img = qrcode.make(url)
        qr_code_img.save(full_path)

        # Return the relative path to the QR code (for use in the template)
        return f"/{full_path.replace('\\', '/')}"  # Convert to a URL-friendly path
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None
