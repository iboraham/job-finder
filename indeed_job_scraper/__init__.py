from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import selenium
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import platform


# Edit the user input
def _edit_terms(txt):
    terms_array = txt.split(", ")
    terms_array = [term.replace(" ", "+") for term in terms_array]
    return terms_array


class Scraper:
    """
    Scraper that finds ["Title", "Location", "Company", "Salary", "Description"]'s of the jobs.
    It is only work for indeed.co.uk.
    Though, this module only works in United Kingdom.
    """

    def __init__(self, search_terms_txt, website="indeed", start_invisible=False):
        if website == "indeed":
            self.df = pd.DataFrame(
                columns=["Title", "Location", "Company", "Salary", "Description"]
            )
        self.website = website
        self.start_invisible = start_invisible
        self.search_terms = _edit_terms(search_terms_txt)
        self.chromeOptions = Options()
        self._start_driver()
        self.stop_flag = False

    def _fetch_company(self):
        try:
            company = self.soup.find(class_="company").text.replace("\n", "").strip()
        except selenium.common.exceptions.NoSuchElementException:
            company = "None"
        return company

    def _fetch_title(self):
        try:
            title = self.soup.find("a", class_="jobtitle").text.replace("\n", "")
        except selenium.common.exceptions.NoSuchElementException:
            title = "None"
        return title

    def _fetch_location(self):
        try:
            location = self.soup.find(class_="location").text
        except selenium.common.exceptions.NoSuchElementException:
            location = "None"
        return location

    # Start driver
    def _start_driver(self):
        if self.start_invisible:
            self.chromeOptions.add_argument("--window-size=1920,1080")
            self.chromeOptions.add_argument("--start-maximized")
            self.chromeOptions.add_argument("--headless")
        else:
            self.chromeOptions.add_argument("--start-maximized")
        if platform.system() == "Windows":
            self.driver = webdriver.Chrome(
                "./driver/chromedriver.exe", chrome_options=self.chromeOptions
            )
        elif platform.system() == "Darwin":
            self.driver = webdriver.Chrome(
                "./driver/chromedriver", chrome_options=self.chromeOptions
            )
        else:
            raise Exception(
                "The program does not support "
                + platform.system()
                + ". Try the latest version"
            )

    # Finding the data frame columns
    def _find_cols(self, job):

        title = self._fetch_title()
        location = self._fetch_location()
        company = self._fetch_company()
        salary = self._fetch_salary()
        job_desc = self._fetch_description(job)

        return title, location, company, salary, job_desc

    # The basic scrap function (Scraping a page)
    def _scrap(self):

        all_jobs = self.driver.find_elements_by_class_name("result")

        for job in all_jobs:
            result_html = job.get_attribute("innerHTML")
            self.soup = BeautifulSoup(result_html, "html.parser")

            self._check_popover()
            title, location, company, salary, job_desc = self._find_cols(job)

            self.df = self.df.append(
                {
                    "Title": title,
                    "Location": location,
                    "Company": company,
                    "Description": job_desc,
                },
                ignore_index=True,
            )

    # Check and close if there is a popover
    def _check_popover(self):
        try:
            close = self.driver.find_element_by_xpath('//*[@id="popover-x"]/a')
            close.click()
        except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.ElementNotInteractableException:
            pass

    # Main Scrap function
    def scrap_data(self):
        for term in self.search_terms:
            self._search_the_term(term)
        self.driver.quit()

    def _accept_cookies(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='onetrust-accept-btn-handler']")
                )
            ).click()
        except selenium.common.exceptions.ElementClickInterceptedException:
            element = self.driver.find_element_by_id("onetrust-accept-btn-handler")
            ed = ActionChains(self.driver)
            ed.move_to_element(element).move_by_offset(0, 5).click().perform()

    def _fetch_salary(self):
        try:
            salary = self.soup.find(class_="salary").text.replace("\n", "")
        except selenium.common.exceptions.NoSuchElementException and AttributeError:
            salary = "None"
        return salary

    def _fetch_description(self, job):
        sum_div = job.find_elements_by_class_name("summary")[0]
        sum_div.click()

        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[0])
        try:
            job_desc = self.driver.find_element_by_id("vjs-desc").text
        except selenium.common.exceptions.NoSuchElementException:
            sum_div.click()
            self.driver.implicitly_wait(2)
            job_desc = self.driver.find_element_by_id("vjs-desc").text
        return job_desc

    def _search_the_term(self, term):
        self._get_the_main_page(term)

        for i in np.arange(0, self.pageCount, 10):
            self._fetch_a_page(i, term)
            if self.pageCount - i <= 10:
                break

    def _find_page_count(self):
        pageCount_txt = self.driver.find_element_by_id("searchCountPages").text
        try:
            pageCount = int(re.match("Page 1 of (\S+) jobs", pageCount_txt).group(1))
        except ValueError:
            pageCount = re.match("Page 1 of (\S+) jobs", pageCount_txt).group(1)
            pageCount = int(pageCount.replace(",", ""))
        print("Total number of jobs available is " + str(pageCount))
        self.pageCount = pageCount

    def _get_the_main_page(self, term):
        url = "https://www.indeed.co.uk/jobs?q=" + term + "&l=United+Kingdom"
        self.driver.get(url)
        try:
            self._find_page_count()
        except selenium.common.exceptions.NoSuchElementException:
            self.driver.quit()
            raise Exception(
                "No result found at keyword " + term + " please try different keywords"
            )

    def _fetch_a_page(self, i, term):
        if self.stop_flag:
            raise Exception("stopped by stop flag")
        if i == 0:
            self._accept_cookies()
        else:
            url = (
                "https://www.indeed.co.uk/jobs?q="
                + term
                + "&l=United+Kingdom&start="
                + str(i)
            )
            self.driver.get(url)
        self.driver.implicitly_wait(4)

        print("Loading " + str(i / self.pageCount * 100) + "%")

        # First check popover then scrap the page
        self._check_popover()
        self._scrap()
