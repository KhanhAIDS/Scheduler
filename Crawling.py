from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = "https://qldt.hust.edu.vn/"
EXPECTED_XPATH_LOGIN = "//button[text()='Đăng nhập']"
EXPECTED_XPATH_OFFICE_365 = '//button[.//b[text()="Office 365"]]'

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get(URL)
driver.delete_all_cookies()
driver.set_window_size(1920, 1080)

time.sleep(2.5)
button = wait.until(EC.presence_of_element_located((By.XPATH, EXPECTED_XPATH_LOGIN)))
# outer_html = button.get_attribute('outerHTML')
button.click()

time.sleep(2.5)
office_button = wait.until(EC.presence_of_element_located((By.XPATH, EXPECTED_XPATH_OFFICE_365)))
# outer_html = office_button.get_attribute('outerHTML')
office_button.click()

time.sleep(2.5)
email_field_xpath = '//input[@type="email" and @name="loginfmt"]'
email_field = wait.until(EC.presence_of_element_located((By.XPATH, email_field_xpath)))
email_field.send_keys("Nhập email trường")  # Replace with email

next_button_xpath = '//input[@type="submit" and @value="Next"]'
next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
next_button.click()

time.sleep(3.5)
password_field_xpath = '//input[@type="password"]'
password_field = wait.until(EC.presence_of_element_located((By.XPATH, password_field_xpath)))
password_field.send_keys("Nhập password email trường")  # Replace with password

sign_in_button_xpath = '//span[contains(text(), "Sign in")]'
sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath)))
sign_in_button.click()

time.sleep(1.5)
final_button_xpath = '/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input'
final_button = wait.until(EC.element_to_be_clickable((By.XPATH, final_button_xpath)))
final_button.click()

time.sleep(10)

def extract_table_data(wait):
    try:
        table_xpath = '/html/body/div[4]/div/div[2]/div[1]/div/div[2]/div[2]/div/div[3]/div/table/tbody[1]'
        table = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))

        rows = table.find_elements(By.XPATH, './tr')
        print(f"[INFO] Number of entries found: {len(rows)}")

        data = []
        for index in range(1, len(rows) + 1):
            entry_data = {}
            try:
                row_xpath = f'{table_xpath}/tr[{index}]'
                row = wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))

                try:
                    entry_data['Value2'] = row.find_element(By.XPATH, './td[2]/div').text
                except Exception:
                    entry_data['Value2'] = ""

                try:
                    try:
                        entry_data['Value3'] = row.find_element(By.XPATH, './td[3]/div/a/p').text
                    except Exception:
                        entry_data['Value3'] = row.find_element(By.XPATH, './td[3]/div/p').text
                except Exception:
                    entry_data['Value3'] = ""

                try:
                    entry_data['Value4'] = row.find_element(By.XPATH, './td[3]/div/b').text
                except Exception:
                    entry_data['Value4'] = ""

                try:
                    entry_data['Value5'] = row.find_element(By.XPATH, './td[5]/div').text
                except Exception:
                    entry_data['Value5'] = ""

                try:
                    entry_data['Value7'] = row.find_element(By.XPATH, './td[7]/div/a').text
                except Exception:
                    entry_data['Value7'] = ""

                data.append(entry_data)

            except Exception as e:
                print(f"[WARNING] Error processing row {index}: {e}")

        with open("table_data.json", "w", encoding="utf-8") as f:
            import json
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("[INFO] Table data saved to 'table_data.json'.")

    except Exception as e:
        print(f"[ERROR] Error while extracting table data: {e}")
        raise

extract_table_data(wait)
driver.quit()