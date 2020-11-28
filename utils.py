from selenium.common.exceptions import WebDriverException
import sys

def get_url(url, driver):
    try:
        driver.get(url)
    except WebDriverException as e:
        print("Error: Chrome not reachable. Exiting the program.", e)
        sys.exit(1)