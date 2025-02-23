import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class YoutubeScraper:
    def __init__(self, username):
        self.username = username
        self.base_url = f"https://www.youtube.com/{username}/shorts"
        self.driver = uc.Chrome()
    
    def get_youtube_shorts_html(self):
        try:
            time.sleep(random.uniform(3, 7))
            self.driver.get(self.base_url)
            # print("sleeping")
            # time.sleep(10000)
            time.sleep(random.uniform(3, 7))
            refuse_cookies = self.driver.find_element(By.XPATH, 
                '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[1]/div/div/button'
            )
            time.sleep(random.uniform(2, 4))
            refuse_cookies.click()
            time.sleep(random.uniform(5, 7))
            html = self.driver.page_source
            self.close()
            return html
        except Exception as e:
            print(f"Erreur lors de la récupération de la page: {e}")
            return None
    
    def extract_shorts_links(self, html):
        soup = BeautifulSoup(html, "html.parser")
        links = []
        try:
            for a_tag in soup.find_all("a", class_="shortsLockupViewModelHostEndpoint reel-item-endpoint"):
                href = a_tag.get("href")
                if href:
                    links.append(f"https://youtube.com{href}")
            return links
        except Exception as e:
            print(f"Error while trying to find videos in html: {e}")

    def get_usernames_from_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                usernames = [line.strip() for line in file.readlines() if line.strip()]
            return usernames
        except FileNotFoundError:
            print(f"Le fichier {file_path} est introuvable.")
            return []
        
    def save_links_to_file(self, links, file_path="to_download.txt"):
        try:
            with open(file_path, "w") as file:
                for link in links:
                    file.write(link + "\n")
            print(f"{len(links)} liens enregistrés dans {file_path}")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement des liens: {e}")
    
    def close(self):
        self.driver.quit()

# Exemple d'utilisation
if __name__ == "__main__":
    username = "@b3nthy"  # Remplace par un nom d'utilisateur valide
    scraper = YoutubeScraper(username)
    html_content = scraper.get_youtube_shorts_html()
    if html_content:
        shorts_links = scraper.extract_shorts_links(html_content)
        print(shorts_links)
    scraper.save_links_to_file(shorts_links)

    # Exemple de lecture d'un fichier d'usernames
    # file_path = "channels.txt"
    # usernames = scraper.get_usernames_from_file(file_path)
    # print(usernames)
    