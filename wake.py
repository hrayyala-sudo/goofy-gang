import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Replace with your actual Streamlit public URL
STREAMLIT_URL = "https://your-app-name.streamlit.app"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

try:
    print(f"Opening {STREAMLIT_URL}...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(STREAMLIT_URL)
    
    wait = WebDriverWait(driver, 10)
    button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes, get this app back up')]"))
    )
    button.click()
    print("Wake button clicked successfully! ✅")
    time.sleep(5)
except Exception as e:
    print("App is likely already awake or button not found:", e)
finally:
    try:
        driver.quit()
    except:
        pass
