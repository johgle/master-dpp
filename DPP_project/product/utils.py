"""
Utilities for the project.
Includes a function to get the local ip adress of the server

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

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