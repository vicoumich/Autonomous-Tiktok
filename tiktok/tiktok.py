import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import random
import pickle
from time import sleep
import inspect
import os
from tiktok.config import (
    PASSWORD,
    USERNAME,
    COOKIES
)
from tiktok.dom_ids import Dom_ids

URL  = "https://www.tiktok.com/login"
URL_POST = "https://www.tiktok.com/upload?lang=fr"
PATH = "C:\\Users\\vicou\Desktop\\code\\code\\TikTok\\chromedriver.exe"
HASHTAGS = ["#tiktok", "#foryou", "#foryoupage", "#fyp", "#viral", "#humour", 
            "#trending", "#tiktokfrance", "#drole", "#funny"]
STR_TAGS = ' '.join(HASHTAGS)

def find_line():
    return inspect.currentframe().f_back.f_lineno

class TikTokControler:

    def __init__(self) -> None:
        self.connected = False
        self.in_home = False
        self.in_upload = False
        options = Options()
        options.page_load_strategy = "normal"
        # Keep windows open
        # options.add_experimental_option("detach", True)
        self.driver = uc.Chrome(options=options)

        # Stealth
        stealth(self.driver,
                languages = ["fr-FR", "fr"],
                vendor = "Google Inc.",
                platform = "Win64",
                webgl_vendor = "Intel Inc.",
                renderer = "Intel Iris OpenGl Engine"
        )
        self.driver.maximize_window()
        self.driver.get(URL)

    def test_element(self, xpath:str, nbline:int):
        """
            Return the element search faster
            than waiting n seconds.
        """
        count = 0
        while count < 70:
            sleep(0.1)
            try:
                return self.driver.find_element(By.XPATH, xpath)
            except:
                pass
            count += 1
        # raise Exception(f"\nImpossible to find the element in line {nbline}.\n")
        print(f"\nImpossible to find the element in line {nbline}.\n")
        sleep(100000)

    def wait_random(self, a=3, b=6):
        sleep(random.uniform(a,b))

    def _save_cookie(self):
        with open(COOKIES, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)
        return self.driver.get_cookies()

    def _load_cookie(self):
        with open(COOKIES, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def _add_description(self, description=STR_TAGS):
        self.wait_random()
        # self.driver.execute_script(
        #     f"document.querySelector('#root > div > div > div.css-fsbw52.ep9i2zp0 > div.css-86gjln.edss2sz5 > div > div > div > div.jsx-1810272162.container > div.jsx-1810272162.main > div:nth-child(2) > div.jsx-1601248207.caption-container.caption-markup-container > div.jsx-1601248207.caption-markup > div.jsx-1601248207.caption-editor > div > div > div > div > div > div > span > span').innerHTML = '{description}';"
        #     )
        caption_field = self.driver.find_element(By.CSS_SELECTOR, Dom_ids.tiktok_description_input)
        caption_field.clear()
        caption_field.send_keys(description)

        self.wait_random()

    def post(self, index_part:int, index:int):
        self.wait_random()
        self.driver.get(URL_POST)

        self.wait_random()
        self.wait_random()
        # self.driver.switch_to.frame(0)

        upload_button = self.test_element(Dom_ids.tiktok_upload_button, find_line())

        self.wait_random()
        print("upload button : \n",upload_button)
        
        ##### TEMP CODE ######
        if index_part != -1:
            #### Initial Code ####
            abspath = os.path.abspath(f"../Videos/Vid{index}/Part_{index_part}.mp4") 
            ######################
        else:
            abspath = os.path.abspath(f"../Videos/Vid{index}/test.mp4")
        ######
        upload_button.send_keys(abspath)
        print(f"\nkey sended, path : {abspath}\n")
        sleep(10)
        publish_button = self.driver.find_element(By.XPATH, Dom_ids.tiktok_publish_button)
        self._add_description()

        while publish_button.get_property('disabled'):
            sleep(0.5)
            publish_button = self.driver.find_element(By.XPATH, Dom_ids.tiktok_publish_button)
        try:
            self.wait_random()
            # Click the button to denie cut video
            self.driver.find_element(By.XPATH, '//*[@id="tux-portal-container"]/div[3]/div/div/div/div/div[2]/div[2]/div[3]/button[2]').click()        
        except:
            pass   

        self.wait_random()
        # title = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div/div[1]/input')
        
        # Ultimate
        publish_button.click()
    
    def login_with_cookies(self):
        if self.connected:
            print("\nAlready connected.\n")
            return
        
        try:
            # Charger la page d'accueil de TikTok
            self.driver.get(URL)
            
            # Charger les cookies
            self._load_cookie()
            print("Cookies loaded successfully.")

            # Rafraîchir la page après avoir ajouté les cookies
            self.driver.refresh()
            sleep(5)

            # Vérifier si l'utilisateur est connecté
            if "login" not in self.driver.current_url:
                self.connected = True
                print("\nConnected using cookies.\n")
                return

            print("Cookies loaded but user is not logged in.")
        except Exception as e:
            print("Error while loading cookies:", e)
        
        # Si les cookies échouent, passer au login classique
        print("Proceeding with login via email and password...")
        
    def connect(self):            
        # CLIQUER SUR LES COOKIE, IMPOSSIBLE A AUTOMATISER
        
        self.wait_random()
        # Get out the cookie Shadow DOM
        self.driver.execute_script(Dom_ids.accept_cookies_button).click()

        # sleep(3)
        # Connect with google account
        # google_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[4]')
        google_button = self.test_element(Dom_ids.google_login_button, find_line())
        google_button.click()

        # Email input filling
        self.wait_random()
        root = self.driver.window_handles[0]
        self.driver.switch_to.window(self.driver.window_handles[1])
        email = self.test_element(Dom_ids.google_email_input, find_line())
        self.wait_random()
        email.send_keys(USERNAME)
        email.send_keys(Keys.ENTER)

        # Password input filling
        password = self.test_element(Dom_ids.google_password_input, find_line())
        str_password = PASSWORD
        self.wait_random()
        password.send_keys(str_password)
        password.send_keys(Keys.ENTER)
        self.wait_random()
        google_accept = self.test_element(Dom_ids.google_accept_button, find_line())
        google_accept.click()

        self.driver.switch_to.window(self.driver.window_handles[0])
        self.connected = True
        self.in_home = True
        # print(self._save_cookie())
        print("\n Connected. \n")
  
    def follow(self, username: str):
        follow_strings = ["Suivre", "Follow"]
        if username[0] == "@":
            username = "@" + username

        self.driver.get(f"https://www.tiktok.com/{username}")
        self.wait_random()
        follow_button = self.driver.find_element(By.XPATH, Dom_ids.tiktok_follow_button)
        
        if follow_button.text in follow_strings:  
            follow_button.click()
        else:
            print(f"Can't follow {username}, statut : {follow_button.text}")
    
    def unfollow(self, username: str):
        unfollow_strings = ["Abonnements"]
        if username[0] == "@":
            username = "@" + username

        self.driver.get(f"https://www.tiktok.com/{username}")
        self.wait_random()
        follow_button = self.driver.find_element(By.XPATH, Dom_ids.tiktok_follow_button)
        
        if follow_button.text in unfollow_strings:  
            follow_button.click()
        else:
            print(f"Can't unfollow {username}, statut : {follow_button.text}")

        



if __name__ =="__main__":
    test = TikTokControler()
    test.connect()
    test.post(-1, 32)
    # for i in range(32,33):
    #     test.post(-1, i)
    #     sleep(random.uniform(2400, 3000))
    input("press enter to close")
    # test.post(1,0)
    
    # for i in range(4):
    #     print(3-i)
    #     sleep(1.11)
    # for x in range(3, 6):
    #     sleep(3)
    #     test.post(x, 5)
    #     print(f"Video {x} SUCCESSFULLY POSTED\n")