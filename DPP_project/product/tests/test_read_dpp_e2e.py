"""
End-to-end test file for reading a Digital Product Passport (DPP).
This file contains automated Selenium tests that simulate a user reading an existing DPP by
(already having scanned the QR code and) being presented with the web interface 
"/product/?id={DPP_ID}". The tests verify that the read process is completed successfully
and that the expected header is displayed.

Declaration of Assistance
This test file was developed with the assistance of GitHub Copilot, which provided suggestions during the coding
process. The author adapted and integrated these suggestions to align with the project's structure and
objectives. All code has been critically reviewed and approved by the author.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import psutil

DJANGO_PID = 10768

def run_single_read_dpp_test():
    driver = webdriver.Chrome()
    # Simulate "scanning" a QR code by directly navigating to the URL with a known DPP ID
    driver.get("http://127.0.0.1:8000/product/?id=ID_DPP_nordic_seat_kitchen_chair")

    start = time.time()

    # Wait until the product page is loaded and key data is visible (max 10 seconds)
    for _ in range(100):
        try:
            title = driver.find_element(By.XPATH, "//h1[contains(text(), 'Digital Product Passport for')]")
            if title.is_displayed():
                break
        except Exception:
            pass
        time.sleep(0.1)
    else:
        driver.quit()
        raise AssertionError("Product page did not load correctly within 10 seconds.")

    elapsed = time.time() - start
    print(f"Read DPP E2E test completed in {elapsed:.2f} seconds")
    driver.quit()
    return elapsed

def test_read_dpp_end_to_end_average():
    N = 20
    times = []
    for i in range(N):
        print(f"Running read test {i+1}/{N} ...")
        elapsed = run_single_read_dpp_test()
        print(f"Test {i+1}: {elapsed:.2f} seconds")
        times.append(elapsed)
    avg = sum(times) / N
    print(f"\nAverage read time over {N} runs: {avg:.2f} seconds")
    print(f"Min: {min(times):.2f}, Max: {max(times):.2f}")

def run_single_read_dpp_test_with_ram():
    proc = psutil.Process(DJANGO_PID)
    mem_before = proc.memory_info().rss / 2**20  # MB

    elapsed = run_single_read_dpp_test()

    mem_after = proc.memory_info().rss / 2**20  # MB
    print(f"RAM used by Django for one read DPP E2E test: {mem_after - mem_before:.2f} MB")
    return elapsed, mem_after - mem_before

def test_read_dpp_ram_usage_average():
    N = 20
    times = []
    ram_usages = []
    ram_usages_dict = {}
    for i in range(N):
        print(f"Running RAM test {i+1}/{N} ...")
        elapsed, ram_used = run_single_read_dpp_test_with_ram()
        times.append(elapsed)
        ram_usages.append(ram_used)
        ram_usages_dict[i+1] = round(ram_used,2)
    avg_time = sum(times) / N
    avg_ram = sum(ram_usages) / N
    print(f"\nAverage read time over {N} runs: {avg_time:.2f} seconds")
    print(f"Average RAM usage over {N} runs: {avg_ram:.2f} MB")
    print(f"Min RAM: {min(ram_usages):.2f}, Max RAM: {max(ram_usages):.2f}")
    print(f"All RAM used with test number:", ram_usages_dict, "\n")
    
    avg_ram_without_warmup = sum(ram_usages[1:]) / (N-1)
    print(f"Average RAM usage over {N-1} runs (without warmup): {avg_ram_without_warmup:.2f} MB")
    print(f"Min RAM (without warmup): {min(ram_usages[1:]):.2f}, Max RAM (without warmup): {max(ram_usages[1:]):.2f}")