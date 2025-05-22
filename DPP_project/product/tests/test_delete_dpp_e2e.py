"""
End-to-end test file for deleting a Digital Product Passport (DPP).
This file contains automated Selenium tests that simulate a user deleting an existing DPP by providing a DPP ID
through the web interface "/delete_dpp". The tests verify that the deletion process completes successfully and
that the expected confirmation is displayed at the web interface.

Declaration of Assistance
This test file was developed with the assistance of GitHub Copilot, which provided suggestions during the coding
process. The author selected, adapted, and integrated these suggestions to align with the project's structure and
objectives. All code has been critically reviewed and approved by the author.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def run_single_delete_dpp_test():
    driver = webdriver.Chrome()

    # --- Create DPP (not timed) ---
    driver.get("http://127.0.0.1:8000/new_dpp/")
    driver.find_element(By.ID, "did").send_keys("ddd738631676985828abef74")
    driver.find_element(By.ID, "wid").send_keys("76466b78737892550146d811")
    driver.find_element(By.ID, "eid").send_keys("789de4812fe20a46c3f3962b")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    # Wait for QR code or success message (not timed)
    for _ in range(150):
        try:
            qr = driver.find_element(By.XPATH, "//img[contains(@src, 'qrcodes')]")
            if qr.is_displayed():
                break
        except Exception:
            pass
        time.sleep(0.1)

    # --- Delete DPP (timed) ---
    driver.get("http://127.0.0.1:8000/delete_dpp/")
    driver.find_element(By.ID, "dpp_id").send_keys("ID_DPP_chair001")
    start = time.time()
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    for _ in range(100):
        try:
            success = driver.find_element(By.XPATH, "//*[contains(text(), 'Success! The passport has been successfully deleted.')]")
            if success.is_displayed():
                break
        except Exception:
            pass
        time.sleep(0.1)
    else:
        driver.quit()
        raise AssertionError("Success message was not shown within 10 seconds.")

    elapsed = time.time() - start
    print(f"Delete DPP E2E test completed in {elapsed:.2f} seconds")
    driver.quit()
    return elapsed

def test_delete_dpp_end_to_end_average():
    N = 20
    times = []
    for i in range(N):
        print(f"Running delete test {i+1}/{N} ...")
        elapsed = run_single_delete_dpp_test()
        print(f"Test {i+1}: {elapsed:.2f} seconds")
        times.append(elapsed)
    avg = sum(times) / N
    print(f"\nAverage delete time over {N} runs: {avg:.2f} seconds")
    print(f"Min: {min(times):.2f}, Max: {max(times):.2f}")