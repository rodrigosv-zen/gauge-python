import os
from getgauge.python import before_suite, after_suite, step
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from uuid import uuid1
from getgauge.python import custom_screenshot_writer
import requests

from step_impl.utils.utils import generate_auth_header
from step_impl.utils.auth_header import auth_header

class Driver:
    instance = None

@before_suite
def init():
    global driver
    options = Options()
    #  By default the chrom instance is launched in
    #  headless mode. Do not pass this option if
    #  you want to see the browser window
    options.add_argument("--headless")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dedv-shm-usage')
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    Driver.instance = webdriver.Chrome(chrome_options=options)

@after_suite
def close():
    Driver.instance.close()

@step("Search for <query>")
def go_to_get_started_page(query):
    try:
        buttons = Driver.instance.find_elements(By.ID, "L2AGLb")
        buttons[0].click()
    except:
        pass

    textbox = Driver.instance.find_element(By.XPATH, "//input[@name='q']")
    textbox.send_keys(query)
    textbox.send_keys(Keys.RETURN)

@step("Go to Google homepage at <url>")
def go_to_gauge_homepage_at(url):
    Driver.instance.get(url)

@step("Take screenshot")
def step_take_screenshot():
    take_screenshot()

# Return a screenshot file name
@custom_screenshot_writer
def take_screenshot():
    image = Driver.instance.get_screenshot_as_png()
    file_name = os.path.join(os.getenv("gauge_screenshots_dir"), "screenshot-{0}.png".format(uuid1().int))
    file = open(file_name, "wb")
    file.write(image)
    return os.path.basename(file_name)

@step("Request GET API <base_url> at <endpoint>")
def get_to_api(base_url, endpoint):
    response = requests.get(f'{base_url}{endpoint}')
    print(response.json())
    assert response.json().get('name')


@step("Ping the Financial Accounts API at to get the <financial_account_uuid> with <institution_name>")
def get_to_api(financial_account, institution_name):
    base_url = 'https://api.dev.zenbusiness.com/financial-accounts/v1/external-bank-accounts/financial-accounts?financial_account_uuid='
    response = requests.get(f'{base_url}{financial_account}', headers=auth_header)
    print(response.json())
    assert response.json().get("institution_name") == institution_name
