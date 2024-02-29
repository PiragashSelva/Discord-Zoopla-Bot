# importing discord-related dependencies
import discord
from discord.ext import commands, tasks
# importing selenium-related dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# importing misc dependencies
import asyncio
from collections import defaultdict
import os
from dotenv import load_dotenv

# loading the token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


class MyClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.web_scraper())

    async def on_ready(self):
        print("Success: Bot is connected!")
        print("-----------------------------------")

    async def web_scraper(self):
        await self.wait_until_ready()
        channel = client.get_channel(1160899091115552788)

        listings_dictionary = defaultdict(
            int
        )  # initialising a dictionary of listings we've already seen
        first_loop = 1  # initialising a variable so we can tell if it's the first loop

        s = Service(r"C:\Program Files (x86)\chromedriver.exe")
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")

        while not self.is_closed():
            driver = webdriver.Chrome(service=s, options=options)
            driver.get(
                "https://www.zoopla.co.uk/to-rent/houses/london/north-west/?added=24_hours&beds_max=4&beds_min=3&include_retirement_homes=false&is_retirement_home=false&polyenc=cwoyH%7Cmx%40tAoRi%40lT&polyenc=gowyHbrm%40bwFxzIccEfkk%40__Att%40saHor%40gqHe~Eex%40ioFeqEujDgPa%60EvsEucAjyDe~El%7DComH~b%40%7DwF%7CzCewB&price_frequency=per_month&price_max=2500&property_sub_type=semi_detached&property_sub_type=detached&property_sub_type=terraced&property_sub_type=bungalow&q=North%20West%20London&radius=0&search_source=refine&section=to-rent&user_alert_id=29363721&view_type=list"
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
            except:  # if the gdpr consent iframe doesn't exist then we continue as usual
                pass

            driver.switch_to.default_content()  # switching back to the default iframe

            counter = 0  # initialising a counter/ resetting the counter
            all_listings = driver.find_elements(
                By.CLASS_NAME, "_1c58w6u2"
            )  # get all the listings inside the class
            for (
                listings
            ) in (
                all_listings
            ):  # for all the listings, check if it's already in the dictionary
                if listings.get_attribute("id") in listings_dictionary:
                    pass  # if in the dictionary, do nothing
                else:
                    counter += 1
                    listings_dictionary[listings.get_attribute("id")] = (
                        1  # if it's not in the dictionary, add it to the dictionary and increase the counter
                    )

            if (
                counter != 0 and first_loop != 1
            ):  # if the counter is non-zero and it's not our first loop, we let the user know
                if counter == 1:
                    await channel.send("THERE'S 1 NEW LISTING!!!")
                else:
                    await channel.send("THERE ARE " + str(counter) + " NEW LISTINGS!!!")

            # listing = driver.find_element(By.CLASS_NAME, '_1c58w6u2')
            # latest_listing = listing.get_attribute("id")

            # if latest_listing != current_listing:
            #    await channel.send("THERE'S A NEW LISTING!!!  id: " + latest_listing)
            #    current_listing = latest_listing #setting the latest listing as the one being compared to from now on

            first_loop = 0
            driver.quit()
            await asyncio.sleep(10)


client = MyClient(command_prefix="!", intents=discord.Intents().all())
client.run(TOKEN)