import os
import pickle
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import config


BASE_URL = "https://hh.ru"


class Main:
    _links: list = []
    driver = webdriver.Edge()
    driver.set_page_load_timeout(10)

    def __init__(self, base_url):
        self.login = config.login
        self.password = config.password
        self.base_url = base_url

    def open_cookie(self):
        with open('cookie.pickle', 'rb') as file:
            cookies = pickle.load(file)
            self.open_page_without_js(BASE_URL)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        return 'Ok'

    def auth(self) -> str:
        self.driver.set_page_load_timeout(5)
        try:
            self.driver.get(f'{BASE_URL}/account/login?backurl=%2F&hhtmFrom=main')
        except TimeoutException:
            self.driver.execute_script("window.stop();")
            login_by_password = self.driver.find_element(By.CSS_SELECTOR, 'button[data-qa="expand-login-by-password"]')
            login_by_password.click()
            username = self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-input-username']")
            username.send_keys(self.login)
            password = self.driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-input-password']")
            password.send_keys(self.password)
            password.send_keys(Keys.ENTER)

        return 'Ok'

    def get_links(self):
        index = 0
        self.driver.set_page_load_timeout(5)

        while True:
            vacancy_search_url = f'{self.base_url}&page={index}'
            try:
                if self.driver.current_url != vacancy_search_url:
                    self.driver.get(vacancy_search_url)

                vacancy_list = self.driver.find_elements(By.CSS_SELECTOR, "a[data-qa='vacancy-serp__vacancy_response']")
                vacancy_count = len(vacancy_list)

                for link in vacancy_list:
                    self._links.append(link.get_attribute('href'))

                print(f'Страница вакансий успешно загружена, страница #{index + 1}')
                index += 1
                if vacancy_count != 50:
                    return

            except TimeoutException:
                self.driver.execute_script("window.stop();")

    def response(self):
        for link in self._links:
            attempt = 0
            while attempt != 2:
                try:
                    if self.driver.current_url != link:
                        self.driver.get(link)

                    try:
                        xpath_letter_button = 'button[data-qa="vacancy-response-letter-toggle"]'
                        letter_button = self.driver.find_element(By.CSS_SELECTOR, xpath_letter_button)
                        letter_button.click()

                        resume_text_selector = f"//*[contains(text(), '{self.resume}')]"
                        resume_button = self.driver.find_element(By.XPATH, resume_text_selector)
                        resume_button.click()

                        xpath_letter = "textarea[data-qa='vacancy-response-popup-form-letter-input']"
                        letter = self.driver.find_element(By.CSS_SELECTOR, xpath_letter)
                        letter.send_keys('Добрый день! Пожалуйста, рассмотрите мою кандидатуру')

                        xpath_submit_button = 'button[data-qa="vacancy-response-submit-popup"]'
                        submit_button = self.driver.find_element(By.CSS_SELECTOR, xpath_submit_button)
                        submit_button.click()
                    except:
                        pass

                    time.sleep(2)

                except TimeoutException:
                    self.driver.execute_script("window.stop();")

                attempt += 1
        print('Отклики на все вакансии успешно оставлены.\nУдачного поиска работы!')

    def save_cookie(self):
        with open('cookie.pickle', 'wb') as cookie:
            self.driver.set_page_load_timeout(100)
            pickle.dump(self.driver.get_cookies(), cookie)
            self.driver.set_page_load_timeout(10)

    def open_page_without_js(self, url):
        try:
            self.driver.get(url)
        except TimeoutException:
            self.driver.execute_script("window.stop();")

    def __del__(self):
        self.driver.quit()


if __name__ == '__main__':
    m = Main(base_url='https://hh.ru/search/vacancy?text=java+%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8'
                      '%D1%81%D1%82&area=1&hhtmFrom=main&hhtmFromLabel=vacancy_search_line')
    status_auth = None

    if not os.path.exists('./cookie.pickle'):
        status_auth = m.auth()
        question_save_cookie = input('Сохранить логин и пароль? (y/n)\n')
        if question_save_cookie == 'y':
            m.save_cookie()
            print('Данные сохранены')
    else:
        status_auth = m.open_cookie()
    if status_auth == 'Ok':
        m.get_links()
        m.response()
        del m
    else:
        del m
