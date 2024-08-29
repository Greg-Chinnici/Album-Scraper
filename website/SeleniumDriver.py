from selenium import webdriver
from selenium.webdriver.chrome.options import Options

selenium_process_name = "SELENIUM SEARCH"

def CreateDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('log-level=1') # so it wont print warnings from websites being mad at headless browsers
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument(f"--process-name={selenium_process_name}")

    driver = webdriver.Chrome(options)
    return driver
