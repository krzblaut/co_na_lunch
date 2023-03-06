from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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


class OtwarteMenu:

    weekday_names = [
        'poniedziałek', 'wtorek', 'środa', 
        'czwartek', 'piątek', 'sobota', 'niedziela'
        ]


    def __init__(self):
        load_dotenv()
        self.username = os.getenv('FACE_USER')
        self.password = os.getenv('FACE_PASSWORD')
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(5)
        self.otwarte_url = 'https://www.facebook.com/OtwarteDrzwi.restaurant'


    def login(self):
        self.driver.get("https://www.facebook.com")
        self.driver.find_elements(
            By.XPATH, 
            "//button[contains(string(), 'Allow essential and optional cookies')]"
            )[0].click()
        self.driver.find_element(By.ID, 'email').send_keys(self.username)
        self.driver.find_element(By.ID, 'pass').send_keys(self.password)
        self.driver.find_elements(By.NAME, 'login')[0].click()


    def find_lunch_menu(self):

        self.driver.get(self.otwarte_url)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((
            By.XPATH, "//*[contains(text(), 'LUNCH')]"))
            )[0].click()
        time.sleep(2)
        elements = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((
            By.XPATH, "//img[@alt='Może być zdjęciem przedstawiającym tekst']"))
            )
        src = elements[-1].get_attribute('src')
        urllib.request.urlretrieve(src, "otwarte_files/lunchmenu.png")


    def get_text_from_image(self, image_path):
        img = Image.open(image_path)        
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.7)
        text = pytesseract.image_to_string(img, lang="pol")
        return text
    

    def get_each_day_menu(self, text):
        delimiters = [
            'PONIEDZIAŁEK', 'WTOREK', 'ŚRODA', 
            'CZWARTEK', 'PIĄTEK', 'danie wegetariańskie'
            ]
        for delimiter in delimiters:
            text = text.replace(delimiter, 'splitter')
        days_menu = text.split('splitter')
        return days_menu[1:-1]

    def get_todays_menu(self):
        self.login()
        self.find_lunch_menu()
        text = self.get_text_from_image('otwarte_files/lunchmenu.png')
        days_menu_list = self.get_each_day_menu(text)
        weekday = datetime.datetime.now().weekday()
        todays_menu = days_menu_list[weekday].replace('\n\n', '\n').replace('\n', '; ')
        return todays_menu

