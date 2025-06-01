"""
End-to-end test file for updating a Digital Product Passport (DPP).
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


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import psutil
import os

DJANGO_PID = 7916

def run_single_update_dpp_test():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:8000/update_dpp/")

    # Form fields
    driver.find_element(By.ID, "dpp_id").send_keys("ID_DPP_nordic_seat_kitchen_chair")
    driver.find_element(By.ID, "timeStampInvalid").send_keys("2029-12-31")
    driver.find_element(By.ID, "actor_id").send_keys("ID_johanne_glende")

    start = time.time()
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Wait for success message and updated details (max 10 seconds)
    for _ in range(100):
        try:
            success = driver.find_element(By.XPATH, "//*[contains(text(), 'Success! The passport has been successfully updated.')]")
            updated_timestamp = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Timestamp Invalid:')]]")
            updated_actor = driver.find_element(By.XPATH, "//li[strong[contains(text(), 'Responsible Actor:')]]")
            if success.is_displayed() and updated_timestamp.is_displayed() and updated_actor.is_displayed():
                break
        except Exception:
            pass
        time.sleep(0.1)
    else:
        driver.quit()
        raise AssertionError("Success message or updated details not shown within 10 seconds.")

    elapsed = time.time() - start
    print(f"Update DPP E2E test completed in {elapsed:.2f} seconds")
    driver.quit()
    return elapsed

def test_update_dpp_end_to_end_average():
    N = 20
    times = []
    for i in range(N):
        print(f"Running update test {i+1}/{N} ...")
        elapsed = run_single_update_dpp_test()
        print(f"Test {i+1}: {elapsed:.2f} seconds")
        times.append(elapsed)
    avg = sum(times) / N
    print(f"\nAverage update time over {N} runs: {avg:.2f} seconds")
    print(f"Min: {min(times):.2f}, Max: {max(times):.2f}")


def run_single_update_dpp_test_with_ram():
    proc = psutil.Process(DJANGO_PID)
    mem_before = proc.memory_info().rss / 2**20  # MB

    elapsed = run_single_update_dpp_test()

    mem_after = proc.memory_info().rss / 2**20  # MB
    print(f"RAM used by Django for one update DPP E2E test: {mem_after - mem_before:.2f} MB")
    return elapsed, mem_after - mem_before

def test_update_dpp_ram_usage_average():
    N = 20
    times = []
    ram_usages = []
    ram_usages_dict = {}
    for i in range(N):
        print(f"Running RAM test {i+1}/{N} ...")
        elapsed, ram_used = run_single_update_dpp_test_with_ram()
        times.append(elapsed)
        ram_usages.append(ram_used)
        ram_usages_dict[i+1] = round(ram_used,2)
    avg_time = sum(times) / N
    avg_ram = sum(ram_usages) / N
    print(f"\nAverage update time over {N} runs: {avg_time:.2f} seconds")
    print(f"Average RAM usage over {N} runs: {avg_ram:.2f} MB")
    print(f"Min RAM: {min(ram_usages):.2f}, Max RAM: {max(ram_usages):.2f}")
    print(f"All RAM used with test number:", ram_usages_dict, "\n")

    avg_ram_without_warmup = sum(ram_usages[1:]) / (N-1)
    print(f"Average RAM usage over {N-1} runs (without warmup): {avg_ram_without_warmup:.2f} MB")
    print(f"Min RAM (without warmup): {min(ram_usages[1:]):.2f}, Max RAM (without warmup): {max(ram_usages[1:]):.2f}")