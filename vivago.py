from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains




def click(element):
    action= ActionChains(driver)
    action.move_to_element(element).click(element).perform()



def vivago(link):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    global driver
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(link)

    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Select a quantity')]")))
    click(driver.find_element(By.XPATH, "//span[contains(text(),'Select a quantity')]"))
    click(driver.find_element(By.XPATH, "//div[contains(text(),'Any')]"))
    driver.find_element(By.XPATH, "//button[contains(text(),'Continue')]").click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(concat(' ',normalize-space(@class),' '),'t-b fs16')]")))

    data_list = list()
    event_name = driver.find_element(By.CSS_SELECTOR, ".l.cBlu1").text
    location = driver.find_element(By.CSS_SELECTOR, ".h.ed-text-overflow").text.split(",")[1]
    date = driver.find_element(By.XPATH, "// span[contains(text(), '(')] / parent::*").text.split("\n")[0].strip()

    while True:
        price_elems = driver.find_elements(By.XPATH,
                                           "//span[contains(concat(' ',normalize-space(@class),' '),'t-b fs16')]")
        block_elems = driver.find_elements(By.XPATH, "//span[contains(text(),'Section:')]/parent::div")
        for price_elem, block_elem in zip(price_elems, block_elems):
            ticket = {
                "event_name": event_name,
                "location": location,
                "date": date,
                "criteria": price_elem.text,
                "block": "",
            }
            try:
                ticket['block'] = block_elem.text.split("|")[1].strip()
            except:
                pass
            data_list.append(ticket)
        try:
            driver.find_element(By.XPATH, "//li[(contains(concat(' ',@class,' '),' js-next')) and not(contains(concat(' ',@class,' '),'v-disabled'))]").click()
        except:
            break


    driver.close()
    return data_list