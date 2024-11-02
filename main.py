import os
import pickle
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import config

BASE_URL = "https://hh.ru"

class JobAutomation:
    def __init__(self, base_url=BASE_URL):
        self.driver = webdriver.Edge()
        self.driver.set_page_load_timeout(10)
        self.base_url = base_url
        self.login = config.login
        self.password = config.password
        self.links = []


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()


    def save_cookies(self):
        """Save cookies to avoid re-authentication."""
        with open('cookie.pickle', 'wb') as file:
            pickle.dump(self.driver.get_cookies(), file)
        print("Cookies saved successfully.")


    def authenticate(self):
        """Authenticate user by login and password."""
        self.driver.get(f'{BASE_URL}/account/login?backurl=%2F&hhtmFrom=main')
        self.driver.execute_script("window.stop();")

        try:
            self.driver.find_element(By.CSS_SELECTOR, 'span[data-qa="expand-login-by-password-text"]').click()
            self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-input-username']").send_keys(self.login)
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-input-password']")
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.ENTER)
            time.sleep(2)
            return True
        except NoSuchElementException:
            print("Authentication elements not found.")
            return False


    def get_job_links(self):
        """Retrieve job links from search pages."""
        page_index = 0
        while True:
            search_url = f'{self.base_url}&page={page_index}'
            self.driver.get(search_url)
            job_links = self.driver.find_elements(By.CSS_SELECTOR, "a[data-qa='vacancy-serp__vacancy_response']")
            
            if not job_links:
                break
            
            for link in job_links:
                self.links.append(link.get_attribute('href'))
            
            print(f'Page {page_index + 1} loaded with {len(job_links)} job listings.')
            page_index += 1
            time.sleep(2)


    def submit_responses(self):
        """Submit responses to all saved job links."""
        for link in self.links:
            self.driver.get(link)
            try:
                self.driver.find_element(By.XPATH, f'//span[@data-qa="resume-title" and text()="{config.job}"]').click()
                self.driver.find_element(By.CSS_SELECTOR, 'button[data-qa="vacancy-response-submit-popup"]').click()
                print(f'Submitted response for {link}')
                time.sleep(2)
            except NoSuchElementException:            
                print(f"Could not submit response for {link}")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    with JobAutomation(base_url=config.base_url) as bot:
        bot.authenticate()
        bot.get_job_links()
        bot.submit_responses()
        print("Job application process completed.")
