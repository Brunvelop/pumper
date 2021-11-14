from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep


class Scraper:
    
    def __init__(self, languaje = 'en', window = False, wait_limit = 180, tries_number = 3,
                driver_path = 'extractors/chromedriver/chromedriver.exe'):
        options = webdriver.ChromeOptions()
        options.add_argument('lang='+ languaje)
        if window:
            options.add_argument("--start-maximized")
        else:
            options.add_argument("--no-sandbox")
            options.add_argument("headless")
            options.add_argument('--disable-dev-shm-usage')  

        self.driver = webdriver.Chrome(
            executable_path=driver_path,
            chrome_options=options)
            
        self.wait_limit = wait_limit
        self.tries_number = tries_number
    
    def close_driver(self):
        self.driver.close()
    
    def open_url(self, url):
        print('Oppening url: {}'.format(url))
        self.driver.get(url)
        #WebDriverWait(self.driver, 1) #.until(EC.presence_of_element_located((By.ID, "myDynamicElement")))
        sleep(2)
        action = ActionChains(self.driver)
        action.send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
        sleep(1)    

    def extract_account_data(self, url):
        self.open_url(url)
        
        table = self.driver.find_element_by_xpath('//div[@id="socialblade-user-content"]/div[5]')
        rows = table.find_elements_by_xpath('div')

        data = self._extract_data_from_rows(rows)

        return data

    def _extract_data_from_rows(self, rows):
        data = []
        for row in rows[0:-1]: #Empty final div

            date = row.text.split('\n')[0]
            followers_str = row.text.split('\n')[3].split(' ')[0]
            followers = int(followers_str.split(',')[0] + followers_str.split(',')[1])

            data.append({
                "date": date,
                "followers": followers 
            })
        return data

class Socialblade():

    def get_twitter_account_data(self, twitter_account):
        scraper = Scraper(window=True)
        url = f'https://socialblade.com/twitter/user/{twitter_account}/monthly'
        data = scraper.extract_account_data(url)
        scraper.close_driver()
        
        return data

s = Socialblade()
print(s.get_twitter_account_data('thetanarena'))
