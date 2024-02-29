# importing discord-related dependencies
import discord
from discord.ext import commands, tasks
import datetime
# importing selenium-related dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# importing misc dependencies
import time
import os
from dotenv import load_dotenv

# loading the token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


class MyClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        channel = client.get_channel(910874215039778902)
        print("Success: Bot is connected!")
        print("-----------------------------------")
        await self.web_scraper.start(channel)

    current_listing = "temp"  # initialising a listing to compare to
    s = Service(r"C:\Program Files (x86)\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")

    @tasks.loop(seconds=20)
    async def web_scraper(self, channel):

        driver = webdriver.Chrome(service=s, options=options)
        driver.get(
            "https://www.zoopla.co.uk/to-rent/property/london/?radius=0&added=24_hours&price_frequency=per_month&polyenc=yadoH%60b%7DXmhsCcjwZoupGungJkh_N%7CbyAoxmKbd%7EEechFlioFy_hA%60%7CwFngj%40neuCftvEle%7CFxw%7EIle%7CFteuLrqGfliOd%7CpC%7EswAoeuCa%7Ep%40mmbF&search_source=to-rent&results_sort=newest_listings&q=London"
        )

        try:
            iframe = WebDriverWait(driver, 5).until(
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
                    (
                        By.XPATH,
                        "//span[contains(text(),'Reject non-essential cookies')]",
                    )
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
        except:
            pass

        driver.switch_to.default_content()

        listing = driver.find_element(By.CLASS_NAME, "_1c58w6u2")
        latest_listing = listing.get_attribute("id")

        if latest_listing != current_listing:
            print(
                "THERE IS A NEW LISTING!!!     Time: "
                + str(time.strftime("%H:%M:%S", time.localtime()))
            )  # print statement to terminal with timestamp
            print("id: " + latest_listing)
            current_listing = latest_listing  # setting the latest listing as the one being compared to from now on

        driver.quit()

        # await channel.send("Testing 1 2 3")


client = MyClient(command_prefix="!", intents=discord.Intents().all())
client.run(TOKEN)