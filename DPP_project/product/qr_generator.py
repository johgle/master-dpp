import qrcode

def generate_qr_code(url, filename):
    """
    Genererer en QR-kode for gitt URL og lagrer den som en bildefil (png).
    """
    # Lag et QRCode-objekt
    img = qrcode.make(url)
    # Lagre bildet som filename
    img.save(filename)
    print(f"QR-kode generert og lagret som {filename}")

if __name__ == "__main__":
    # Eks. URL
    my_url = "http://192.168.10.181:8000/product?id=stol_123"

    # Velg filnavn for lagring
    output_file = "stol_123_qrcode.png"

    generate_qr_code(my_url, output_file)
