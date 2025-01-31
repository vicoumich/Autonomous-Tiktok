# from distutils.command.upload import upload
# from lib2to3.pgen2.driver import Driver
# from platform import platform
# from selenium import webdriver
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
from config import (
    PASSWORD,
    USERNAME,
    COOKIES
)

URL  = "https://www.tiktok.com/login"
URL_POST = "https://www.tiktok.com/upload?lang=fr"
PATH = "C:\\Users\\vicou\Desktop\\code\\code\\TikTok\\chromedriver.exe"
HASHTAGS = ["#tiktok", "#foryou", "#foryoupage", "#fyp", "#viral", "#tiktokindia", 
            "#trending", "#tiktokfrance", "#comedy", "#funny"]
STR_TAGS = ' '.join(HASHTAGS)

def find_line():
    return inspect.currentframe().f_back.f_lineno

class TikTokControler:

    def __init__(self) -> None:
        self.connected = False
        self.in_home = False
        self.in_upload = False
        options = Options()
        options.add_argument("start-maximized")

        # Chrome is controlled by automated test software
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--mute-audio")

        # Avoiding detection
        options.add_argument('--disable-blink-features=AutomationControlled')

        # Default User Profile
        options.add_argument("--profile-directory=Default")
        options.add_argument("--user-data-dir=C:/Users/Admin/AppData/Local/Google/Chrome/User Data")

        self.driver = uc.Chrome()

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
        raise Exception(f"\nImpossible to find the element in line {nbline}.\n")

    def wait_random(self):
        sleep(random.uniform(1,4))

    def _save_cookie(self):
        with open(COOKIES, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)
        return self.driver.get_cookies()

    def _load_cookie(self):
        with open(COOKIES, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def post(self, index_part:int, index:int):
        # self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/div[1]').click()
        self.wait_random()
        self.driver.get(URL_POST)

        self.wait_random()
        self.driver.switch_to.frame(0)

        publish_button = self.test_element('//*[@id="root"]/div/div/div/div/div[2]/div[2]/div[8]/div[2]/button', find_line())

        upload_button = self.test_element('/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/input', find_line())
        self.wait_random()
        upload_button.send_keys(f"C:\\Users\\vicou\\Desktop\\code\\POSTED\\Autonomous_Tiktok\\Videos\\Vid{index}\\Part_{index_part}_{STR_TAGS}.mp4")

        while publish_button.get_property('disabled'):
            self.wait_random()
            publish_button = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div[2]/div[8]/div[2]/button')
        try:
            self.wait_random()
            # Click the button to denie cut video
            self.driver.find_element(By.XPATH, '//*[@id="tux-portal-container"]/div[3]/div/div/div/div/div[2]/div[2]/div[3]/button[2]').click()        
        except:
            pass   

        self.wait_random()
        # title = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div/div[1]/input')
        
        # Ultimate
        self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div[2]/div[8]/div[2]/button').click()
    
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
        self.driver.execute_script('''return document.querySelector("body > tiktok-cookie-banner").shadowRoot.querySelector("div > div.button-wrapper > button:nth-child(2)")''').click()

        # sleep(3)
        # Connect with google account
        # google_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[4]')
        google_button = self.test_element('/html/body/div[1]/div/div[2]/div/div/div/div[5]/div[2]', find_line())
        google_button.click()

        self.wait_random()
        root = self.driver.window_handles[0]
        self.driver.switch_to.window(self.driver.window_handles[1])

        email = self.test_element("/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input", find_line())
        self.wait_random()
        email.send_keys(USERNAME)
        email.send_keys(Keys.ENTER)

        password = self.test_element("/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input", find_line())
        str_password = PASSWORD
        self.wait_random()
        password.send_keys(str_password)
        password.send_keys(Keys.ENTER)
        self.wait_random()
        google_accept = self.test_element('//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[2]/div/div/button', find_line())
        google_accept.click()

        self.driver.switch_to.window(self.driver.window_handles[0])
        self.connected = True
        self.in_home = True
        print(self._save_cookie())
        print("\n Connected. \n")
  
    def follow_mass(self, n:int):
        sleep(3)
        self.driver.get("https://www.tiktok.com/fr")
        sleep(3)
        
        comments_button = self.test_element('//*[@id="app"]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[2]/button[2]')
        comments_button.click()
        #finir



if __name__ =="__main__":
    test = TikTokControler()
    test.connect()
    # test.post(1,0)
    sleep(100000)
    # for i in range(4):
    #     print(3-i)
    #     sleep(1.11)
    # for x in range(3, 6):
    #     sleep(3)
    #     test.post(x, 5)
    #     print(f"Video {x} SUCCESSFULLY POSTED\n")