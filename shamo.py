from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time


class ShamoMenu:


    def __init__(self):
        load_dotenv()
        self.username = os.getenv('FACE_USER')
        self.password = os.getenv('FACE_PASSWORD')
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(5)
        self.shamo_wall = 'https://www.facebook.com/RestauracjaShamo'


    def get_todays_menu(self):
        self.login()
        post = self.get_last_post()
        todays_menu = self.extract_lunch_menu(post)
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


    def get_last_post(self):
        self.driver.get(self.shamo_wall)
        all_posts = self.driver.find_elements(
            By.CSS_SELECTOR, '[data-pagelet="ProfileTimeline"]')
        latest_post = all_posts[0].text
        return latest_post
    

    def extract_lunch_menu(self, post):
        date = post.split('·')[0].split('SHAMO')[-1]
        menu = post.split(')')[1].split('*')[0].replace('\n', '').replace(':', '').replace(' ', '', 1)
        if 'godz' in date:
            if int(date.split('godz')[0]) < 12:
                todays_menu = menu
        else:
            todays_menu = 'brak danych'
        return todays_menu
