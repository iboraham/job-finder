import math
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
import re
import selenium
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import platform


class Scraper:
    """
    This class defines the basic interface called by the tree builders.

    These methods will be called by the parser:
      reset()
      feed(markup)

    The tree builder may call these methods from its feed() implementation:
      handle_starttag(name, attrs) # See note about return value
      handle_endtag(name)
      handle_data(data) # Appends to the current data node
      endData(containerClass=NavigableString) # Ends the current data node

    No matter how complicated the underlying parser is, you should be
    able to build a tree using 'start tag' events, 'end tag' events,
    'data' events, and "done with data" events.

    If you encounter an empty-element tag (aka a self-closing tag,
    like HTML's <br> tag), call handle_starttag and then
    handle_endtag.
    """

    def __init__(self, search_terms_txt, website='indeed', start_invisible=False):
        self.website = website
        self.start_invisible = start_invisible
        self.search_terms = search_terms_txt
        self.chromeOptions = Options()

    # Edit the user input
    def _edit_terms(txt):
        txt.replace(' ', '+')
        terms_array = txt.split(',')
        return terms_array

    # Start driver
    def _start_driver(self):
        if self.start_invisible:
            self.chromeOptions.add_argument("--headless")
        else:
            self.chromeOptions.add_argument("--start-maximized")
        if platform.system() == 'Windows':
            self.driver = webdriver.Chrome("./driver/chromedriver.exe", chrome_options=self.chromeOptions)
        elif platform.system() == 'Darwin':
            self.driver = webdriver.Chrome("./driver/chromedriver", chrome_options=self.chromeOptions)

    # Finding the data frame columns
    def _find_cols(self, soup, job):
        # Title
        try:
            title = soup.find("a", class_="jobtitle").text.replace('\n', '')
        except:
            title = 'None'
        # location
        try:
            location = soup.find(class_="location").text
        except:
            location = 'None'
        # company
        try:
            company = soup.find(class_="company").text.replace("\n", "").strip()
        except:
            company = 'None'
        # salary
        try:
            salary = soup.find(class_="salaryText").text.replace('\n', '').strip()
        except:
            salary = 'None'
        # Description

        sum_div = job.find_elements_by_class_name("jobtitle")[0]
        try:
            sum_div.click()
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(driver.window_handles[0])
            job_desc = self.driver.find_element_by_id('vjs-desc').text
        except:
            sum_div.click()
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(driver.window_handles[0])
            self.driver.implicitly_wait(3)
            job_desc = self.driver.find_element_by_id('vjs-desc').text

        return title, location, company, salary, job_desc

    # The basic scrap function (Scraping a page)
    def _scrap(self, driver, df):
        try:
            driver.find_element_by_xpath('//*[@id="resultsCol"]')
        except selenium.common.exceptions.NoSuchElementException:
            pass

        all_jobs = driver.find_elements_by_class_name('result')

        for job in all_jobs:
            result_html = job.get_attribute('innerHTML')
            soup = BeautifulSoup(result_html, 'html.parser')

            _check_popover(driver)
            title, location, company, salary, job_desc = _find_cols(soup, job, driver)

            df = df.append({'Title': title, 'Location': location, 'Company': company,
                            "Description": job_desc}, ignore_index=True)
        return df

    # Check and close if there is a popover
    def _check_popover(self):
        try:
            close = self.driver.find_element_by_xpath('//*[@id="popover-x"]/a')
            close.click()
        except:
            pass

    # Main Scrap function
    def scrap_data(self):
        df = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Description"])
        self._edit_terms()
        for search in search_terms:
            for i in np.arange(0, pageCount, 10):
                url = "https://www.indeed.co.uk/jobs?q=" + search + "&l=United+Kingdom&start=" + str(i)
                driver.get(url)
                print("Query has started")
                driver.implicitly_wait(6)
                if i == 0:
                    try:
                        pageCount_txt = driver.find_element_by_id('searchCountPages').text
                    except selenium.common.exceptions.NoSuchElementException:
                        driver.quit()
                        return 'No result found at keyword ' + search + ' please try different keywords'
                    try:
                        pageCount = int(re.match('Page 1 of (\S+) jobs', pageCount_txt).group(1))
                    except ValueError:
                        pageCount = re.match('Page 1 of (\S+) jobs', pageCount_txt).group(1)
                        pageCount = int(pageCount.replace(',', ''))
                    print("Total number of jobs available is " + str(pageCount))

                print('Loading ' + str(i / pageCount * 100) + '%')

                # First check popover then scrap the page
                _check_popover(driver)
                df = _scrap(driver, i, df)

                if pageCount - i <= 10:
                    break

        driver.quit()
        return df
