import os
import requests
import pandas as pd

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# Directory to store the data we scrape
DATA_DIR = 'data/'
if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)

options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", DATA_DIR)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv")
driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', firefox_options=options)
url = 'https://www.football-data.co.uk/englandm.php'
driver.get(url)

all_links = driver.find_elements_by_xpath('/html/body/table[5]/tbody/tr[2]/td[3]/a')

for link in all_links:
    url = link.get_attribute('href')
    # Check link is for Premier League
    if url[-5] == '0':
        season = url[-11:-7]
        df = pd.read_csv(url)
        df['season'] = season
        df.dropna(how='all', inplace=True)
        
        fname = 'season' + season + '.csv'
        print(f'Saving: {fname}')
        filepath = os.path.join(DATA_DIR, fname)
        df.to_csv(filepath)


        # response = requests.get(url)
        # b_string = response.text.encode('utf-8')
        # text = b_string.decode('utf-8')
        # fname = f'season{url[-11:-7]}.csv'
        # print(f'Saving: {fname}')
        # with open(os.path.join(DATA_DIR, fname), 'w', encoding='utf-8') as f:
        #     f.write(text)

           
driver.close()

