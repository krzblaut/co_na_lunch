import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from PIL import Image
import pytesseract
from dotenv import load_dotenv


class DokiMenu:

    folder_path = '/home/krzychu/facebook_bot/doki_screenshots'


    def __init__(self):

        load_dotenv()
        self.username = os.getenv('FACE_USER')
        self.password = os.getenv('FACE_PASSWORD')
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.stories = 'https://www.facebook.com/stories/'


    def get_todays_menu(self):
        self.login()
        self.take_screenshots()
        stories = self.get_lunch_stories()
        menu = self.clean_text(stories[-1])
        self.remove_temp_files()
        return menu
    

    def login(self):
        self.driver.get("https://www.facebook.com")
        self.driver.find_elements(By.XPATH, "//button[contains(string(), 'Allow essential and optional cookies')]")[0].click()
        self.driver.find_element(By.ID, 'email').send_keys(self.username)
        self.driver.find_element(By.ID, 'pass').send_keys(self.password)
        self.driver.find_elements(By.NAME, 'login')[0].click()


    def take_screenshots(self):
        self.driver.get(self.stories)
        self.driver.find_elements(By.XPATH, "//*[contains(text(), 'DOKI gastrobar')]")[1].click()
        i=0
        while True: 
            self.driver.save_screenshot(f'doki_screenshots/image{i}.png')
            i+=1
            time.sleep(0.2)
            curr_url = self.driver.current_url
            if 'stories' not in curr_url:
                self.driver.close()
                break


    def text_from_image(self, image_path):
        left = 1200
        top = 90
        right = 1730
        bottom = 1000
        img = Image.open(image_path)
        cropped_image = img.crop((left, top, right, bottom))
        text = pytesseract.image_to_string(cropped_image, lang="pol")
        return text
    

    def get_lunch_stories(self):
        lunch_stories = []
        for i in range(1000):
            try:
                path = f'doki_screenshots/image{i}.png'
                text = self.text_from_image(path)
                if 'lunch' in text and 'DOKI' in text:
                    lunch_stories.append([path, text])
            except FileNotFoundError:
                break
        return lunch_stories[-1]
    

    def clean_text(self, text):
        text = text.split('\n\n')
        text = text[3] + ' + ' + text[4]
        text = text.replace('\n', ' ')
        return text    
    

    def remove_temp_files(self):
        if os.path.exists(self.folder_path):
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            pass

    
# doki = DokiMenu()
# doki.login()
# doki.take_screenshots()
# stories = doki.get_lunch_stories()
# text = doki.text_from_image('doki_2_opcje.png')
# print(text)
# print(doki.clean_text(text))

