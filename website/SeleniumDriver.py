from selenium import webdriver
from selenium.webdriver.wpewebkit.webdriver import WebDriver

selenium_process_name = "SELENIUM SEARCH"


def CreateDriver():
    driver = Chrome()
    print(driver.name, driver.session_id)
    return driver

def Chrome():
    options = webdriver.ChromeOptions()
    options.add_argument("headless=new")  # runs in background
    options.add_argument("log-level=1")  # so it wont print warnings from websites being mad at headless browsers
    options.add_argument("--no-sandbox")  # less secure, but faster
    options.add_argument("--disable-extensions")  # not needed
    options.add_argument(f"--process-name={selenium_process_name}")  # for cleanup later

    print(options.arguments)
    return webdriver.Chrome(options)

def Edge():
    options = webdriver.EdgeOptions()
    options.add_argument("headless=new")  # runs in background
    options.add_argument("--log-level=SEVERE")  # so it wont print warnings from websites being mad at headless browsers
    return webdriver.ChromiumEdge(options)
