import qrcode
import os

def generate_qr_code(ip_adress, DID, WID, EID):
    """
    Generate Qr code when called, likely when new passport is created and added to KB.
    """
    url = f"http://{ip_adress}:8000/product?id={DID}_{WID}_{EID}"
    filename = f"{DID}_{WID}_{EID}_qrcode.png"

    # Define the full path to the qrcodes folder
    qr_code_folder = os.path.join(
        os.path.dirname(__file__), '..', 'media', 'qrcodes'
    )
    full_path = os.path.join(qr_code_folder, filename)

    # Ensure the directory exists
    os.makedirs(qr_code_folder, exist_ok=True)

    # Generate and save the QR code image
    qr_code_img = qrcode.make(url)
    qr_code_img.save(full_path)
