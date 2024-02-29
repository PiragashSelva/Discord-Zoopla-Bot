# importing selenium-related dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# importing misc dependencies
import time
from collections import defaultdict


listings_dictionary = defaultdict(
    int
)  # initialising a dictionary of listings we've already seen
listings_dictionary["listing_60561824"] = (
    1  # pre-loading the dictionary with the listings we've already seen
)

s = Service(r"C:\Program Files (x86)\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")

while True:

    driver = webdriver.Chrome(service=s, options=options)
    driver.get(
        "https://www.zoopla.co.uk/to-rent/property/london/?radius=0&added=24_hours&price_frequency=per_month&polyenc=yadoH%60b%7DXmhsCcjwZoupGungJkh_N%7CbyAoxmKbd%7EEechFlioFy_hA%60%7CwFngj%40neuCftvEle%7CFxw%7EIle%7CFteuLrqGfliOd%7CpC%7EswAoeuCa%7Ep%40mmbF&search_source=to-rent&results_sort=newest_listings&q=London"
    )

    try:  # if the gdpr consent iframe exists then we execute this code to get rid of it
        iframe = WebDriverWait(
            driver, 5
        ).until(  # waiting to see if the gdpr consent iframe loads up
            EC.presence_of_element_located(
                (By.XPATH, "//iframe[@id='gdpr-consent-notice']")
            )
        )
        driver.switch_to.frame(iframe)

        ################################# REJECT NON-ESSENTIAL COOKIES #########################################
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(),'Manage preferences')]")
            )
        )
        element.click()

        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(),'Reject non-essential cookies')]")
            )
        )
        element.click()
        ########################################################################################################

        ###################################### ACCEPT ALL COOKIES ##############################################
        # element = WebDriverWait(driver,5).until(
        #    EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Accept all cookies')]"))
        # )
        # element.click()
        ########################################################################################################
    except:  # if the gdpr consent iframe doesn't exist then we continue as usual
        pass

    driver.switch_to.default_content()  # switching back to the default iframe

    counter = 0  # initialising a counter/ resetting the counter
    all_listings = driver.find_elements(
        By.CLASS_NAME, "_1c58w6u2"
    )  # get all the listings inside the class
    for (
        listings
    ) in all_listings:  # for all the listings, check if it's already in the dictionary
        if listings.get_attribute("id") in listings_dictionary:
            pass  # if in the dictionary, do nothing
        else:
            counter += 1
            listings_dictionary[listings.get_attribute("id")] = (
                1  # if it's not in the dictionary, add it to the dictionary and increase the counter
            )

    if counter != 0:  # if the counter is non-zero, we let the user know
        if counter == 1:
            print("THERE'S 1 NEW LISTING!!!")
        else:
            print("THERE ARE " + str(counter) + " NEW LISTINGS!!!")

    driver.quit()
    time.sleep(5)