import os
import csv
import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

"""
cols = [,Date,HomeTeam,AwayTeam,FTR,HTGS,ATGS,HTGC,ATGC,HTP,ATP,HM1,HM2,HM3,HM4,HM5,
        AM1,AM2,AM3,AM4,AM5,MW,HTFormPtsStr,ATFormPtsStr,HTFormPts,ATFormPts,
        HTWinStreak3,HTWinStreak5,HTLossStreak3,HTLossStreak5,ATWinStreak3,ATWinStreak5,
        ATLossStreak3,ATLossStreak5,HTGD,ATGD,DiffPts,DiffFormPts,DiffLP]

This module scrapes bet 365 English Premier League fixtures
and creates a csv file where each row is an upcoming fixture
"""

DATA_DIR = 'data/'



class FixtureScraper:
    """
    TODO: Create full module with subclasses and methods

    returns a numpy array where each instance is upcoming fixture and teams
    previous result data
    """


    def __init__(self):
        options = Options()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", DATA_DIR)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv")
        self.driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', firefox_options=options)

        url = 'https://s5.sir.sportradar.com/bet365/en/1/season/66441/fixtures'
        self.driver.get(url)
        self.driver.implicitly_wait(10)


    def get_fixtures(self):
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

    def close_driver(self):
        self.driver.close()

# scraper = FixtureScraper()
# scraper.get_fixtures()
# scraper.close_driver()