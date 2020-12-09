"""
File for utility functions
Authors: Edward Mattout & Daniella Grimberg
"""

from selenium.common.exceptions import WebDriverException
import sys


def get_url(url, driver):
    """
    Function uses driver to retrieve URL . Exits with 1 if driver not reachable
    :param url: url to retrieve
    :param driver: driver
    :return:
    """
    try:
        driver.get(url)
    except WebDriverException as e:
        print("Error: Chrome not reachable. Exiting the program.", e)
        sys.exit(1)
