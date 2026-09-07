import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Replace with your actual Streamlit public URL
STREAMLIT_URL = "https://goofy-gang.streamlit.app"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    print(f"Opening {STREAMLIT_URL}...")
    driver.get(STREAMLIT_URL)
    
    wait = WebDriverWait(driver, 10)
    button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes, get this app back up')]"))
    )
    button.click()
    time.sleep(5)
except Exception as e:
finally:
    driver.quit()
