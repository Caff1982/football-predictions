import os
import csv
import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


DATA_DIR = 'data/'


class Scraper:
    """
    Base class to initialize Selenium browser that other classes can
    inherit from
    """
    def __init__(self):
        options = Options()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", DATA_DIR)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv")
        self.driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',
                                        firefox_options=options)

    def close_driver(self):
        self.driver.close()


class FixtureScraper(Scraper):
    """
    Gets information on upcoming fixtures and returns results as Pandas DataFrame
    """
    def __init__(self):
        super().__init__()
        self.url = 'https://s5.sir.sportradar.com/bet365/en/1/season/66441/fixtures'

    def get_fixtures(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        date = self.driver.find_element_by_xpath('//*[@id="sr-container"]/div/div/div[4]/div/div/div/div/div[2]/div/div/div/table/tbody/tr[2]/td[1]').text

        all_fixtures = self.driver.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[4]/div/div/div/div/div[2]/div/div/div/table/tbody/tr')
        fixtures = []
        for fixture in all_fixtures[2:]:
            fixture_list = fixture.text.split('\n')
            if len(fixture_list) > 6:
                home_team = fixture_list[1]
                away_team = fixture_list[3]
                home_odds = fixture_list[4]
                draw_odds = fixture_list[5]
                away_odds = fixture_list[6]

                season = 1920

                fixtures.append([date, home_team, away_team, home_odds, 
                                 draw_odds, away_odds, season])
        return pd.DataFrame(fixtures, columns=['Date', 'HomeTeam', 'AwayTeam', 
                                               'B365H', 'B365D', 'B365A', 'season'])


class LeagueScraper(Scraper):
    """
    Scrapes csv files of previous seasons and saves them to DATA_DIR.
    N.B there is a ParserError saving season 0405 but this is not needed.
    """
    def __init__(self):
        super().__init__()
        self.url = 'https://www.football-data.co.uk/englandm.php'

    def get_league_positions(self):

        self.driver.get(self.url)

        all_links = self.driver.find_elements_by_xpath('/html/body/table[5]/tbody/tr[2]/td[3]/a')

        for link in all_links:
            url = link.get_attribute('href')
            # Check link is for Premier League
            if url[-5] == '0':
                season = url[-11:-7]
                try:
                    df = pd.read_csv(url)
                except Exception as e:
                    print(f'Error saving season: {season}')
                    break

                df['season'] = season
                df.dropna(how='all', inplace=True)
                
                fname = 'season' + season + '.csv'
                print(f'Saving: {fname}')
                filepath = os.path.join(DATA_DIR, fname)
                df.to_csv(filepath)

class LeaguePositionScraper(Scraper):
    """
    Scrapes league positions from Wikipedia and saves them to DATA_DIR
    """
    def __init__(self):
        super().__init__()
        self.filepath = os.path.join(DATA_DIR, 'league_standings.csv')

        with open(os.path.join(self.filepath), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Season', 'Position', 'Team'])

    def run(self):
        base_url = 'https://en.wikipedia.org/wiki/20'
        for i in range(6, 19):
            if i < 9:
                url = base_url + '0' + str(i) + '-0' + str(i+1) + '_Premier_League'
            elif i == 9:
                url = base_url + '0' + str(i) + '-' + str(i+1) + '_Premier_League'
            else:
                url = base_url + str(i) + '-' + str(i+1) + '_Premier_League'
            
            self.get_league_positions(self, url)

    def get_league_positions(self, idx, url):
        self.driver.get(url)
        self.driver.implicitly_wait(1)
        print(f'Scraping {url}')

        # In these two seasons the data is further down the page
        if idx in (12, 16):
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
                writer.writerow([idx, position, team])
