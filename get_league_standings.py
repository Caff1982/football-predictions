import csv
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class LeagueStandings:

    def __init__(self):
        self.data_dir = 'data/'
        self.filepath = 'data/league_standings.csv'
        self.options = Options()
        self.options.set_preference("browser.download.manager.showWhenStarting", False)
        self.options.set_preference("browser.download.dir", self.data_dir)
        self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv")
        self.driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', firefox_options=self.options)
        

        with open(self.filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Season', 'Position', 'Team'])

    def get_league_standings(self, i, url):
        self.driver.get(url)
        print(f'Scraping {url}')
        # Fow two seasons the data is further down the page
        if i in (12, 16):
            all_rows = self.driver.find_elements_by_xpath('/html/body/div[3]/div[3]/div[4]/div/table[6]/tbody/tr')
        else:
            all_rows = self.driver.find_elements_by_xpath('/html/body/div[3]/div[3]/div[4]/div/table[5]/tbody/tr')

        with open(self.filepath, 'a') as f:
            writer = csv.writer(f)

            for row in all_rows[1:]:
                split_row = row.text.split()
                position = split_row[0]
                team = split_row[1] 
                if team == 'Wolverhampton':
                    team = 'Wolves'
                elif team == 'Manchester':
                    if split_row[2] == 'City':
                        team = 'Man City'
                    elif split_row[2] == 'United':
                        team = 'Man United'
                writer.writerow([i, position, team])

    def close_driver(self):
        self.driver.close()


if __name__ == '__main__':
    base_url = 'https://en.wikipedia.org/wiki/20'
    scraper = LeagueStandings()

    for i in range(6, 19):
        if i < 9:
            url = base_url + '0' + str(i) + '-0' + str(i+1) + '_Premier_League'
        elif i == 9:
            url = base_url + '0' + str(i) + '-' + str(i+1) + '_Premier_League'
        else:
            url = base_url + str(i) + '-' + str(i+1) + '_Premier_League'
        
        scraper.get_league_standings(i, url)

    scraper.close_driver()