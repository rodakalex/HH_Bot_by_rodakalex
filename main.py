import time
from urllib import parse
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import config

'''
TODO:
    1. Дополнить роли
'''
roles = {
    1: 'Event-manager',
    2: 'PR-manager'
}


class Main:
    _links: list = []
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(10)

    def __init__(self, vacancy: str, role: int, salary: int = 0, only_with_salary: bool = False, schedules: list = None):
        self.schedule = ''

        for schedule in schedules:
            self.schedule += f"schedule={schedule}&"

        if not len(schedules):
            self.schedule = self.schedule[0:len(self.schedule)]

        self.login: str = config.login
        self.password: str = config.password
        self.vacancy: str = parse.quote_plus(vacancy)
        self.salary: int = salary
        self.only_with_salary = only_with_salary
        self.role = role
        
    def auth(self) -> str:
        self.driver.set_page_load_timeout(5)
        try:
            self.driver.get('https://hh.ru/account/login?backurl=%2F&hhtmFrom=main')
        except TimeoutException:
            self.driver.execute_script("window.stop();")
            login_by_password = self.driver.find_element(By.XPATH, "//button[@data-qa='expand-login-by-password']")
            login_by_password.click()
            username = self.driver.find_element(By.XPATH, "//input[@data-qa='login-input-username']")
            username.send_keys(self.login)
            password = self.driver.find_element(By.XPATH, "//input[@data-qa='login-input-password']")
            password.send_keys(self.password)
            password.send_keys(Keys.ENTER)

        return 'Ok'

    def get_links(self):
        index = 0
        self.driver.set_page_load_timeout(5)

        while True:
            page_link = (f'https://hh.ru/search/vacancy?professional_role={self.role}&schedule=remote'
                         f'&search_field=name&search_field=company_name&search_field=description'
                         f'&enable_snippets=true&salary={self.salary}&only_with_salary='
                         f'{self.only_with_salary}&text='
                         f'{self.vacancy}&from=suggest_post&L_save_area=true&page={index}')
            try:
                if self.driver.current_url != page_link:
                    self.driver.get(page_link)

                vacancy_list = self.driver.find_elements(By.XPATH, "//a[@data-qa='vacancy-serp__vacancy_response']")
                vacancy_count = len(vacancy_list)

                for link in vacancy_list:
                    self._links.append(link.get_attribute('href'))

                print(f'Страница вакансий успешно загружена, страница #{index}')
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
                        xpath_letter_button = '//button[@data-qa="vacancy-response-letter-toggle"]'
                        letter_button = self.driver.find_element(By.XPATH, xpath_letter_button)
                        letter_button.click()
                    except NoSuchElementException:
                        pass

                    xpath_letter = "//textarea[@data-qa='vacancy-response-popup-form-letter-input']"
                    letter = self.driver.find_element(By.XPATH, xpath_letter)
                    letter.send_keys('Добрый день! Пожалуйста, рассмотрите мою кандидатуру')

                    xpath_submit_button = '//button[@data-qa="vacancy-response-submit-popup"]'
                    submit_button = self.driver.find_element(By.XPATH, xpath_submit_button)
                    submit_button.click()

                    time.sleep(2)

                except TimeoutException:
                    self.driver.execute_script("window.stop();")

                attempt += 1
        print('Отклики на все вакансии успешно оставлены!')

    def __del__(self):
        self.driver.close()
        exit()


if __name__ == '__main__':
    # Пример использования
    schedules = ['remote', 'fullDay']
    m = Main(vacancy='1С', salary=300000, only_with_salary=True, role=96, schedules=schedules)
    status_auth = m.auth()
    if status_auth == 'Ok':
        m.get_links()
        m.response()
        del m
    else:
        del m
