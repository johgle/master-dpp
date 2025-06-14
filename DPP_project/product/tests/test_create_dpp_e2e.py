"""
End-to-end test file for creating a Digital Product Passport (DPP).
This file contains automated Selenium tests that simulate a user creating a new DPP by providing a Document ID (DID),
Workspace ID (WID), and Element ID (EID) through the web interface "/new_dpp". The tests verify that the creation
process completes successfully and that the expected confirmation and QR code are displayed.

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

DJANGO_PID = 24928


def run_single_create_dpp_test():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:8000/new_dpp/")

    #Form fields
    driver.find_element(By.ID, "did").send_keys("ddd738631676985828abef74")
    driver.find_element(By.ID, "wid").send_keys("76466b78737892550146d811")
    driver.find_element(By.ID, "eid").send_keys("789de4812fe20a46c3f3962b")

    start = time.time()
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Wait for QR code success message (max 10 seconds)
    for _ in range(100):
        try:
            qr = driver.find_element(By.XPATH, "//img[contains(@src, 'qrcodes')]")
            dpp_success = driver.find_element(By.XPATH, "//*[contains(text(), 'Success! The passport has been created.')]")
            if qr.is_displayed() and dpp_success.is_displayed():
                break
        except Exception:
            pass
        time.sleep(0.1)

    else:
        driver.quit()
        raise AssertionError("QR code or Success message was not shown in 10 seconds.")

    elapsed = time.time() - start
    driver.quit()
    return elapsed

def test_create_dpp_end_to_end_average():
    N = 20
    times = []
    for i in range(N):
        print(f"Kjører test {i+1}/{N} ...")
        elapsed = run_single_create_dpp_test()
        print(f"Test {i+1}: {elapsed:.2f} sekunder")
        times.append(elapsed)
    avg = sum(times) / N
    print(f"\nGjennomsnittstid over {N} tester: {avg:.2f} sekunder")
    print(f"Min: {min(times):.2f}, Maks: {max(times):.2f}")


def run_single_create_dpp_test_with_ram():
    proc = psutil.Process(DJANGO_PID)
    mem_before = proc.memory_info().rss / 2**20  # MB

    elapsed = run_single_create_dpp_test()

    mem_after = proc.memory_info().rss / 2**20  # MB
    print(f"RAM used by Django for one create DPP E2E test: {mem_after - mem_before:.2f} MB")
    return elapsed, mem_after - mem_before

def test_create_dpp_ram_usage_average():
    N = 20
    times = []
    ram_usages = []
    ram_usages_dict = {}

    for i in range(N):
        print(f"Running RAM test {i+1}/{N} ...")
        elapsed, ram_used = run_single_create_dpp_test_with_ram()
        times.append(elapsed)
        ram_usages.append(ram_used)
        ram_usages_dict[i+1] = round(ram_used,2)

    avg_time = sum(times) / N
    avg_ram = sum(ram_usages) / N
    print(f"\nAverage create time over {N} runs: {avg_time:.2f} seconds")
    print(f"Average RAM usage over {N} runs: {avg_ram:.2f} MB")
    print(f"Min RAM: {min(ram_usages):.2f}, Max RAM: {max(ram_usages):.2f}")
    print(f"All RAM used with test number:", ram_usages_dict, "\n")

    # Calculate without warm-up bias
    avg_ram_without_warmup = sum(ram_usages[1:]) / (N-1)
    print(f"Average RAM usage over {N-1} runs (without warmup): {avg_ram_without_warmup:.2f} MB")
    print(f"Min RAM (without warmup): {min(ram_usages[1:]):.2f}, Max RAM (without warmup): {max(ram_usages[1:]):.2f}")

