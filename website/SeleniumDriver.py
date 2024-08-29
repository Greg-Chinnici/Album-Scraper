from selenium import webdriver

selenium_process_name = "SELENIUM SEARCH"

def CreateDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless') # runs in background
    options.add_argument('log-level=1') # so it wont print warnings from websites being mad at headless browsers
    options.add_argument('--no-sandbox') # less secure, but faster
    options.add_argument("--disable-extensions") # not needed
    options.add_argument(f"--process-name={selenium_process_name}") # for cleanup later

    driver = webdriver.Chrome(options)
    return driver
