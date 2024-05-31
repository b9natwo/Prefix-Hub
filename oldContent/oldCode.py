import discord
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
import pytz
import os
import json
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

# Variables Needed For Change

leaks_channel_id = None # Where the bot will send the leaks
error_channel_id = None # Insert a Channel Id for the bot to send errors to (in case something goes wrong)
Email = None # For Login Purposes
Password = None # For Login Purposes
TOKEN = None # Discord Bot Token

leak_channels_guilds = {}

def login_to_website(email, password):
    # Set up Selenium WebDriver with appropriate options
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)

    # Load the login page and fill in the credentials
    driver.get("https://leaked.cx/login")
    driver.find_element(By.NAME, "login").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div/div/div/div/div/div/form/div[1]/dl/dd/div/div[2]/button/span").click()
    # Wait for the login process to complete
    driver.implicitly_wait(10)
    return driver

async def scrape_leaks():
    global error_channel

    try: # All Leaks
                # Log into the website
        driver = login_to_website(f"{Email}", f"{Password}")

        # Navigate to the Juice WRLD leaks section
        driver.get("https://leaked.cx/forums/hiphopleaks/")

        # Wait for the page to load
        await asyncio.sleep(5)

        # Scrape the page for new leaks
        soup = BeautifulSoup(driver.page_source, "html.parser")
        leaks = soup.find_all("div", class_="structItemContainer-group js-threadList")

        # Iterate through the leaks and send Discord embed messages
        for leak in leaks:
            leak_title = leak.find("a", attrs = {"class" : ""}).text.strip()
            leak_url = leak.find("a", attrs= {"class" : ""})["href"]
            leak_datetime = leak.find("time", attrs={"class": "u-dt"}).text.strip()
            leak_tag = leak.find("span", attrs={"dir": "auto"}).text.strip()

            if leak_tag == "LEAK":
                leak_title = leak.find("a", attrs = {"class" : ""}).text.strip() + " [LEAK]"

            if leak_tag == "EARLY":
                leak_title = leak.find("a", attrs = {"class" : ""}).text.strip() + " [EARLY]"

            if leak_tag == "SNIPPET":
                leak_title = leak.find("a", attrs = {"class" : ""}).text.strip() + " [SNIPPET]"

            if leak_tag == "DEMO":
                leak_title = leak.find("a", attrs = {"class" : ""}).text.strip() + " [DEMO]"

            if leak_tag == "OLD LEAK":
                leak_title = leak.find("a", attrs = {"class" : ""}).text.strip() + " [OLD LEAK]"

            # Check if the leak has already been sent
            if not is_duplicate(leak_title):
                # Get a random Juice WRLD image online as the thumbnail
                thumbnail_url = None

                role_id = " "

                get_section = leak.find("div", attrs={"class":"structItem-title"})

                get_tags = get_section.find_all("span", attrs={"dir":"auto"})

                for tag in get_tags:
                    k = tag.get_text()
                    if k == "JUICE WRLD":
                        role_id = None # Juice Role (For Pinging Purposes)
                        thumbnail_url = get_random_juice_wrld_image()
                    if k == "LIL UZI VERT":
                        role_id = None # Uzi Role (For Pinging Purposes)
                        thumbnail_url = get_random_lil_uzi_vert_image()
                    if k == "KANYE WEST":
                        role_id = None # Kanye Role (For Pinging Purposes)
                        thumbnail_url = get_random_kanye_west_image()
                    if k == "TRAVIS SCOTT":
                        thumbnail_url = get_random_travis_scott_image()
                        role_id = None # Travis Role (For Pinging Purposes)
                    if k == "THE WEEKND":
                        role_id = None # Weeknd Role (For Pinging Purposes)
                        thumbnail_url = get_random_the_weeknd_image()
                    if k == "PLAYBOI CARTI":
                        role_id = None # Carti Role (For Pinging Purposes)
                        thumbnail_url = get_random_playboi_carti_image()
                    if k == "DRAKE":
                        role_id = None # Drake Role (For Pinging Purposes)
                        thumbnail_url = get_random_drake_image()
                    if k == "LIL WAYNE":
                        thumbnail_url = get_random_lil_wayne_image()
                        role_id = None # Wayne Role (For Pinging Purposes)
                    if k == "YOUNG THUG":
                        thumbnail_url = get_random_young_thug_image()
                        role_id = None # Thug Role (For Pinging Purposes)
                    if k == "MAC MILLER":
                        thumbnail_url = get_random_mac_miller_image()
                        role_id = None # Mac Miller Role (For Pinging Purposes)
                    if k == "MIGOS":
                        thumbnail_url = get_random_migos_image()
                        role_id = None # Migos Role (For Pinging Purposes)

                    if "Yeat" in leak_title: # FOR CUSTOM PREFIX PURPOSES, THIS IS WHAT YOU'LL HAVE TO PUT.
                        role_id = None # Yeat Role (For Pinging Purposes)
                        thumbnail_url = get_random_yeat_image()

                channel = bot.get_channel(leaks_channel_id)

                embed = discord.Embed(title=leak_title, url=f"https://leaked.cx{leak_url}", color=discord.Color.random())
                embed.set_thumbnail(url=thumbnail_url)
                embed.set_footer(text=f"Leaked | {leak_datetime}")

                # Send the embed message to the specified channel
                if role_id == " ":
                    print("No Role")
                else:
                    await channel.send(f"<@&{role_id}>")
                await channel.send(embed=embed)
                # Store the sent leak to avoid duplicates
                store_leak(leak_title)

        # Close the Selenium WebDriver
        driver.quit()

    except Exception as e:
        # Send the error message to the error channel
        if error_channel is not None:
            await error_channel.send(f"An error occurred while scraping leaks: {str(e)}")

def is_duplicate(leak_title):
    if os.path.exists("sent_leaks.json"):
        with open("sent_leaks.json") as file:
            sent_leaks = json.load(file)
            return leak_title in sent_leaks
