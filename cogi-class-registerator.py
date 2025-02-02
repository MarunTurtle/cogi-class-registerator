from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import os
import time
import datetime

def wait_and_click(by, value):
    """ Wait for an element to be clickable and then click it. """
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
    except TimeoutException:
        print(f"Timeout occurred when trying to click {value}. Waiting for manual action.")
        input("Check the issue and press Enter to continue...")

def wait_and_click_by_text(text):
    """ Wait for the link with specified text to be clickable and then click it. """
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, text))
        )
        element.click()
    except TimeoutException:
        print(f"Timeout occurred when trying to click on text: {text}. Waiting for manual action.")
        input("Check the issue and press Enter to continue...")

def refresh_and_click(by, value):
    """Wait for an element to be clickable and then click it, refreshing the page if the element is not found."""
    while True:
        try:
            # Attempt to find and click the element within 20 seconds
            element = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            break  # Exit the loop if the click was successful
        except TimeoutException:
            # If the element isn't found, refresh the page and try again
            print(f"Element with {value} not found. Refreshing the page...")
            driver.refresh()

def attempt_previous_step_and_retry(by, value):
    """Attempt to perform the previous step and then retry clicking the current step element."""
    while True:
        try:
            # Attempt to find and click the element
            element = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            break  # Exit the loop if successful
        except TimeoutException:
            print(f"Element with {value} not found. Going back to perform the previous step...")
            # Go back to the previous page
            driver.back()
            print("Went Back")
            driver.refresh()
            print("Refreshed")
            # Perform the previous step
            try:
                wait_and_click(By.CSS_SELECTOR, "a[data-seq='254']")
                print("Clicked using data-seq.")
            except (NoSuchElementException, TimeoutException):
                # If data-seq is not found or the element is not clickable, use text to find and click
                course_text = "[초급 4차] 심리적 응급처치(이론 및 실습)"
                wait_and_click_by_text(course_text)
                print("data-seq not found. Clicked using link text.")
            # Navigate forward or reload to retry the step
            driver.forward()  # Assumes that forward navigation leads to the correct page

def handle_popup():
    try:
        # Wait up to 10 seconds for the popup to be visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "closeBtn2")))
        print("Popup detected with confirm button.")

        # Click the '확인' button to close or confirm the popup
        driver.find_element(By.ID, "closeBtn2").click()
        print("Popup '확인' button clicked.")
    except TimeoutException:
        print("No popup appeared within the timeout period.")
        input("Check the issue and press Enter to continue...")

def wait_until_target_time(target_time):
    """Wait until the target time (datetime object) is reached."""
    now = datetime.datetime.now()
    while now < target_time:
        print(f'{now} Waiting for target time...')
        time.sleep(0.1)
        now = datetime.datetime.now()
    print(f"Reached target time: {now}, proceeding with next Step.")

def handle_popup2(driver):
    try:
        # Wait up to 10 seconds for the alert to be present
        WebDriverWait(driver, 10).until(EC.alert_is_present())

        # Switch to the alert
        alert = driver.switch_to.alert

        # Press the 'OK' button
        alert.accept()
        print("Popup OK button clicked.")
    except NoAlertPresentException:
        print("No popup appeared within the timeout period.")

# Setup WebDriver with UserAgent
options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(options=options)

# Set the target time
target_time1 = datetime.datetime(2024, 4, 22, 8, 55, 0)
target_time2 = datetime.datetime(2024, 4, 22, 9, 0, 0)

try:
    # Step 1: Go to the website
    driver.get('https://edu.nct.go.kr/member/eduLoginForm.do')

    # Wait until the target time
    wait_until_target_time(target_time1)

    # Step 2: Log in using the provided credentials
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "inpId")))
    driver.find_element(By.ID, "inpId").send_keys("judy0902")
    driver.find_element(By.ID, "inpPw").send_keys("dmswls092!")
    wait_and_click(By.ID, "loginFormBtn")  # Ensures the login button is clickable before clicking

    # Step 3: Click the 확인 button (if necessary, add wait to ensure the button is visible)
    wait_and_click(By.ID, "closeBtn2")

    # Step 4: Click Go under 교육신청
    wait_and_click(By.CSS_SELECTOR, "a[href='/eduAplc/regEduList.do']")

    # Wait until the target time
    wait_until_target_time(target_time2)

    # Step 5: Attempt to click on the specific course using data-seq
    try:
        wait_and_click(By.CSS_SELECTOR, "a[data-seq='254']")
        print("Clicked using data-seq.")
    except (NoSuchElementException, TimeoutException):
        # If data-seq is not found or the element is not clickable, use text to find and click
        course_text = "[초급 5차] 심리적 응급처치(이론 및 실습)"
        wait_and_click_by_text(course_text)
        print("data-seq not found. Clicked using link text.")

    # Step 6: Click the 초급과정 신청하기 button
    attempt_previous_step_and_retry(By.ID, "AplcBtn")

    # Step 7: Check the checkbox for 개인정보 수집 이용에 동의함
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkbox")))
    driver.find_element(By.ID, "checkbox").click()

    # Step 8: Type in "간호사" for the position
    driver.find_element(By.NAME, "position").send_keys("간호사")

    # Step 9: Check the checkbox for 확인함
    driver.find_element(By.ID, "confirm").click()

    # Step 10: Click the 신청하기 button
    wait_and_click(By.ID, "addBtn")

    handle_popup2(driver)

finally:
    # This will keep the browser open until you manually close it.
    input("Press any key to exit...")

