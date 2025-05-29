"""
Stresstest for creating multiple Digital Product Passports at once.
This file contains automated Selenium tests that simulate a user updating an existing DPP by providing a DPP ID,
a new timestamp, and a new actor ID through the web interface "/update_dpp". The tests verify that the update process
completes successfully and that the expected confirmation and updated information are displayed.

Declaration of Assistance
This test file was developed with the assistance of GitHub Copilot, which provided suggestions during the coding
process. The author adapted and integrated these suggestions to align with the project's structure and
objectives. All code has been critically reviewed and approved by the author.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

import requests
import concurrent.futures
import json
import time
import psutil

DJANGO_PID = 23780
proc = psutil.Process(DJANGO_PID)

with open("product/onshape_codes/generated_chairs.json") as f:
    chairs = json.load(f)
number = len(chairs)

def create_dpp(chair):
    payload = {
        "did": chair["did"],
        "wid": chair["wid"],
        "eid": chair["eid"]
    }
    start = time.time()
    try:
        response = requests.post("http://127.0.0.1:8000/new_dpp/", data=payload)
        elapsed = time.time() - start
        return {
            "document_name": chair["document_name"],
            "status": response.status_code,
            "elapsed": elapsed,
            "error": None
        }
    except Exception as e:
        elapsed = time.time() - start
        return {
            "document_name": chair["document_name"],
            "status": None,
            "elapsed": elapsed,
            "error": str(e)
        }

mem_before = proc.memory_info().rss / 2**20  # MB
start_time = time.time()

results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=number) as executor:
    futures = [executor.submit(create_dpp, chair) for chair in chairs[:number]]
    for future in concurrent.futures.as_completed(futures):
        results.append(future.result())

elapsed = time.time() - start_time
mem_after = proc.memory_info().rss / 2**20  # MB

print(f"\nCreated {number} DPPs in {elapsed:.2f} seconds")
print(f"RAM grew by {mem_after - mem_before:.2f} MB\n")

for r in results:
    print(f"{r['document_name']}: Status {r['status']}, Time {r['elapsed']:.2f}s, Error: {r['error']}")

# Optionally, print summary stats
success = sum(1 for r in results if r['status'] == 200)
print(f"\nSuccess: {success}/{number}")