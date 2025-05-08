"""
Onshape API example for getting data from Onshape CAD models.
This example uses the Onshape API to fetch data about a CAD model.
It provides functions to get the materials, volume and mass of a product, as a start.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

import os, uuid, hmac, hashlib, base64, datetime, requests, urllib.parse, json


# ---------- API KEYS --------------
# Make sure to set your Onshape API keys as environment variables
ACCESS = os.getenv("ONSHAPE_API_ACCESS_KEY")
SECRET = os.getenv("ONSHAPE_API_SECRET_KEY")

# Create signed headers for the API request
def signed_headers(method:str, url:str, ctype:str = ""):
    """Returnes Date, On-Nonce og Authorization-header for named url."""
    parsed = urllib.parse.urlparse(url)
    path   = parsed.path
    query  = parsed.query

    nonce = uuid.uuid4().hex
    date  = datetime.datetime.now(datetime.UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")
    # ctype = "application/json"

    to_sign = "\n".join([
        method.lower(), nonce.lower(), date.lower(),
        ctype.lower(), path.lower(), query.lower(), ""
    ]).encode()
    # sig = hmac.new(SECRET.encode(), to_sign.encode(), hashlib.sha256).digest()
    # sig_b64 = base64.b64encode(sig).decode()
    sig_b64 = base64.b64encode(hmac.new(SECRET.encode(), to_sign, hashlib.sha256).digest()).decode()

    headers = {
        "Date": date,
        "On-Nonce": nonce,
        "Accept": "application/json",
        "Authorization": f"On {ACCESS}:HmacSHA256:{sig_b64}",
    }

    # Content-Type only when actually sending body
    if ctype:
        headers["Content-Type"] = ctype
    return headers


# Choose a folder name for your possible JSON dumps
DATA_DIR = "onshape_json_data"

# ----------------  ID FROM URLs  -----------------------------
DID_stol = "3cc9b7f1331165f8fa1d4630"  # Document ID
WID_stol = "3ec8b42b563ac643e55281f2"  # Workspace ID
EID_stol = "f0f23b975a63a60a8e3c1e2a"  # Element ID

DID_chair = "ddd738631676985828abef74"  # Document ID
WID_chair = "76466b78737892550146d811"  # Workspace ID
EID_chair = "789de4812fe20a46c3f3962b"  # Element ID

DID = DID_chair # Document ID
WID = WID_chair # Workspace ID
EID = EID_chair # Element ID
BASE = "https://cad.onshape.com/api" # Base URL for Onshape API

# --------------- URLs FOR APIs ------------------
urls = {
    "url_partstudios_feature": f"{BASE}/partstudios/d/{DID}/w/{WID}/e/{EID}/features",
    "url_partstudios_massproperties": f"{BASE}/partstudios/d/{DID}/w/{WID}/e/{EID}/massproperties",
    "url_partstudios_boundingboxes": f"{BASE}/partstudios/d/{DID}/w/{WID}/e/{EID}/boundingboxes",
    "url_partstudios_bodydetails": f"{BASE}/partstudios/d/{DID}/w/{WID}/e/{EID}/bodydetails",
    "url_metadata": f"{BASE}/metadata/d/{DID}/w/{WID}/e/{EID}",
    "url_parts": f"{BASE}/parts/d/{DID}/w/{WID}/e/{EID}",
    # "url_part_massproperties": f"{BASE}/parts/d/{DID}/w/{WID}/e/{EID}/partid/{PID}/massproperties", #this needs a partId
}


def write_data_to_file():
    """Fetch data from Onshape API and write to JSON files."""
    os.makedirs(DATA_DIR, exist_ok=True)


    for url_name, url in urls.items():
        h = signed_headers("GET", url)
        resp = requests.get(url, headers=h)

        print(resp.status_code)

        if resp.ok:
            data = resp.json()

            # Write JSON-data to file
            filename = f"CHAIR_onshape_data_{url_name}.json"
            filepath = os.path.join(DATA_DIR, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Data lagret i {filepath}")
        else:
            print("Kunne ikke hente data:", resp.text)

def write_data_to_file_from_single_api_url(url_name:str, url:str):
    """Fetch data from Onshape API and write to JSON files."""
    os.makedirs(DATA_DIR, exist_ok=True)
    h = signed_headers("GET", url)
    resp = requests.get(url, headers=h)

    print(resp.status_code)

    if resp.ok:
        data = resp.json()

        # Write JSON-data to file
        filename = f"CHAIR_onshape_data_{url_name}.json"
        filepath = os.path.join(DATA_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data lagret i {filepath}")
    else:
        print("Kunne ikke hente data:", resp.text)

def get_api_data(url:str):
    """Fetch data from Onshape API and return as json response."""
    h = signed_headers("GET", url)
    resp = requests.get(url, headers=h)

    # print(resp.status_code)

    if resp.ok:
        data = resp.json()
        # print("Data hentet fra API:", url)
    else:
        print("Kunne ikke hente data:", resp.text)
    return data

def get_product_parts(DID:str, WID:str, EID:str):
    """Returns parsed part data for the given product from the API."""
    return get_api_data(f"{BASE}/parts/d/{DID}/w/{WID}/e/{EID}") #.json response


def get_product_materials(DID:str, WID:str, EID:str):
    """Return ({partId: material_or_None}, sorted_unique_materials)"""
    parts_data = get_product_parts(DID, WID, EID)

    material_per_part = {}
    for p in parts_data:
        part_id = p["partId"]
        display_name = p["material"]["displayName"] if p.get("material") else None
        material_per_part[part_id] = display_name

    all_materials = sorted({m for m in material_per_part.values() if m})
    return material_per_part, all_materials

def get_product_mass(DID:str, WID:str, EID:str):
    """Return mass from return-object from api."""
    parts_data = get_product_parts(DID, WID, EID)

    mass_kg_by_part = {}
    for p in parts_data:
        part_id = p["partId"]
        part_massproperties_data = get_api_data(f"{BASE}/parts/d/{DID}/w/{WID}/e/{EID}/partid/{part_id}/massproperties")
        part_mass = part_massproperties_data["bodies"][part_id]["mass"][0] #nominal mass
        mass_kg_by_part[part_id] = part_mass #nominal mass
    
    # total_mass_all_parts = sum(mass_kg_by_part.values())
    
    partstudios_massproperties_data = get_api_data(f"{BASE}/partstudios/d/{DID}/w/{WID}/e/{EID}/massproperties") #.json file
    total_mass = partstudios_massproperties_data["bodies"]["-all-"]["mass"][0] #total nominal mass
    
    return mass_kg_by_part, total_mass #total mass of all parts in kg

def get_product_volume(DID:str, WID:str, EID:str):
    """Return volume from return-object from api."""
    parts_data = get_product_parts(DID, WID, EID)

    volume_by_part = {}
    for p in parts_data:
        part_id = p["partId"]
        part_massproperties_data = get_api_data(f"{BASE}/parts/d/{DID}/w/{WID}/e/{EID}/partid/{part_id}/massproperties")
        part_volume = part_massproperties_data["bodies"][part_id]["volume"][0] #nominal volume
        volume_by_part[part_id] = part_volume

    # total_volume_all_parts = sum(volume_by_part.values())

    partstudios_massproperties_data = get_api_data(f"{BASE}/partstudios/d/{DID}/w/{WID}/e/{EID}/massproperties") #.json file
    total_volume = partstudios_massproperties_data["bodies"]["-all-"]["volume"][0] #total nominal volume
    
    return volume_by_part, total_volume

def get_document_owner(DID:str):
    """Return name of owner of document."""
    metadata_data = get_api_data(f"{BASE}/documents/{DID}") #.json file
    owner_name = metadata_data["owner"]["name"]
    return owner_name

def get_document_creator(DID:str):
    """Return name of creator of document."""
    metadata_data = get_api_data(f"{BASE}/documents/{DID}") #.json file
    creator_name = metadata_data["createdBy"]["name"]
    return creator_name

def get_document_name(DID:str):
    """Return name of document."""
    metadata_data = get_api_data(f"{BASE}/documents/{DID}") #.json file
    document_name = metadata_data["name"]
    return document_name



# write_data_to_file()
# write_data_to_file_from_single_api_url("url_documents", f"{BASE}/documents/{DID}")
# print("materials:", get_product_materials(DID,WID,EID)[0],
#       "\nsorted unique materials:", get_product_materials(DID,WID,EID)[1])
# print()
# print("mass:", get_product_mass(DID,WID,EID)[0],
#       "\ntotal mass:", get_product_mass(DID,WID,EID)[1])
# print()
# print("volume:", get_product_volume(DID,WID,EID)[0],
#       "\ntotal volume:", get_product_volume(DID,WID,EID)[1])

# print("owner:", get_document_owner(DID))
# print("creator:", get_document_creator(DID))
# print("document name:", get_document_name(DID))





### -------------------- OLD ------------------------- ###
# import requests 
# import json

# # Assemble the URL for the API call 
# # api_url = "https://cad.onshape.com/api/v10/documents/ddd738631676985828abef74"
# # api_url = "https://cad.onshape.com/api/v10/documents/3cc9b7f1331165f8fa1d4630" #stol1
# # api_url = "https://cad.onshape.com/api/v10/featurestudios/d/ddd738631676985828abef74/w/76466b78737892550146d811/e/789de4812fe20a46c3f3962b" #chair.py
# api_url = "https://cad.onshape.com/api/v10/featurestudios/d/3cc9b7f1331165f8fa1d4630/w/3ec8b42b563ac643e55281f2/e/f0f23b975a63a60a8e3c1e2a" #stol1


# #e60c4803eaf2ac8be492c18e"
# """
# Det er denne URLen som bestemmer hvilket produkt vi skal hente data fra.
# I fremtiden må man her kunne sende inn en parameter, feks en productID
# som bestemmer hvilken modell data skal hentes fra.
# """

# # Optional query parameters can be assigned 
# params = {}

# # Use the encoded authorization string you created from your API Keys.
# api_keys = 'V0V6dEgyVG1PUFhudU5EcmFYeHVTWXdMOlhkdkkwckZYVmxiUXFvem1hbVphMEFxRjR5c2tJaThzeWJNYUVPazZRenEzVnhoRQ'

# # # Define the header for the request 
# # headers = {'Accept': 'application/json;charset=UTF-8;qs=0.09',
# #           'Content-Type': 'application/json'}

# import base64

# auth_string = f"api:{api_keys}"
# encoded_auth = base64.b64encode(auth_string.encode()).decode()

# headers = {
#     "Authorization": f"Basic {encoded_auth}",
#     "Accept": "application/json",
#     'Content-Type': 'application/json'
# }

# # Put everything together to make the API request 
# response = requests.get(api_url, 
#                        params=params, 
#                        auth=("api", api_keys), 
#                        headers=headers)

# # Convert the response to formatted JSON and print the `name` property
# # print(json.dumps(response.json(), indent=4))
# if response.status_code == 200:
#     print(json.dumps(response.json(), indent=4))
# else:
#     print(f"Feil! Statuskode: {response.status_code}")
#     print(f"Feilmelding: {response.text}")
