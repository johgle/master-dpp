import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def run_single_create_dpp_test():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:8000/new_dpp/")
    driver.find_element(By.ID, "did").send_keys("ddd738631676985828abef74")
    driver.find_element(By.ID, "wid").send_keys("76466b78737892550146d811")
    driver.find_element(By.ID, "eid").send_keys("789de4812fe20a46c3f3962b")

    start = time.time()
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

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