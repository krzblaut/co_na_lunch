from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import urllib.request
import os
import io
import time
from PIL import Image, ImageEnhance
import pytesseract
import numpy as np
import datetime


class DrukarniaMenu:

    message = "Dzień dobry, co dzisiaj oferują Państwo na lunch?"
    druk_autoresponse = "Dziękujemy za wiadomość. Staramy się odpowiadać"

    def __init__(self):
        load_dotenv()
        self.username = os.getenv('FACE_USER')
        self.password = os.getenv('FACE_PASSWORD')
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(5)
        self.drukarnia_mess = 'https://www.facebook.com/messages/t/139860586167007/'


    def get_todays_menu(self):
        self.login()
        todays_menu = self.check_response()
        return todays_menu


    def login(self):
        self.driver.get("https://www.facebook.com")
        self.driver.find_elements(
            By.XPATH, 
            "//button[contains(string(), 'Allow essential and optional cookies')]"
            )[0].click()
        self.driver.find_element(By.ID, 'email').send_keys(self.username)
        self.driver.find_element(By.ID, 'pass').send_keys(self.password)
        self.driver.find_elements(By.NAME, 'login')[0].click()
        time.sleep(2)

    
    def send_message(self):
        self.driver.get(self.drukarnia_mess)
        textbox = self.driver.find_element(By.CSS_SELECTOR, '[role="textbox"]')
        textbox.send_keys(self.message)
        textbox.send_keys(Keys.RETURN)


    def check_response(self):
        self.driver.get(self.drukarnia_mess)
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, '[class="__fb-light-mode x1n2onr6"]')
        last_response = elements[-1].text
        if self.druk_autoresponse in last_response:
            lunch_menu = "brak danych"
        else:
            lunch_menu = last_response
            lunch_menu.lowercase().replace('dzień dobry', '')
        return lunch_menu
        
