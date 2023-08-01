import time
from urllib import parse
from selenium.common import TimeoutException
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

    def __init__(self, vacancy: str, role: int, salary: int = 0, only_with_salary: bool = False):
        self.login: str = config.login
        self.password: str = config.password
        self.vacancy: str = parse.quote_plus(vacancy)
        self.salary: int = salary
        self.only_with_salary = only_with_salary
        self.role = role

    def auth(self):
        attempt = 0
        while attempt != 3:
            try:
                self.driver.implicitly_wait(1)
                self.driver.get('https://hh.ru/account/login?backurl=%2F&hhtmFrom=main')
                login_by_password = self.driver.find_element(By.XPATH, "//button[@data-qa='expand-login-by-password']")
                login_by_password.click()
                username = self.driver.find_element(By.XPATH, "//input[@data-qa='login-input-username']")
                username.send_keys(config.login)
                password = self.driver.find_element(By.XPATH, "//input[@data-qa='login-input-password']")
                password.send_keys(config.password)
                password.send_keys(Keys.ENTER)
                print('Успешная попытка авторизации')
                return True

            except TimeoutException:
                attempt += 1
                print(f'Неудачная попытка авторизации, #{attempt}')

        print('Авторизация неудачна')
        return False

    def get_links(self):
        index = 0
        self.driver.set_page_load_timeout(20)

        while True:
            attempt = 1
            while attempt != 3:
                try:
                    self.driver.get(f'https://hh.ru/search/vacancy?professional_role={self.role}&schedule=remote&'
                                    f'search_field=name&search_field=company_name&search_field=description&'
                                    f'enable_snippets=true'
                                    f'&salary=300000&only_with_salary={self.only_with_salary}&text={self.vacancy}'
                                    f'&from=suggest_post&L_save_area=true&page={index}')
                    vacancy_list = self.driver.find_elements(By.XPATH, "//a[@data-qa='vacancy-serp__vacancy_response']")
                    vacancy_count = len(vacancy_list)
                    for link in vacancy_list:
                        self._links.append(link.get_attribute('href'))
                    print(f'Страница вакансий успешно загружена, страница #{index}')
                    index += 1
                    if vacancy_count != 50:
                        return

                except TimeoutException:
                    print(f'Страница с вакансиями неудачно загружена, попытка #{attempt}')
                    attempt += 1

    def response(self):
        for link in self._links:
            try:
                self.driver.get(link)
            except TimeoutException:
                pass
            finally:
                submit_button = self.driver.find_element(By.XPATH, '//button[@data-qa="vacancy-response-submit-popup"]')
                submit_button.click()
                time.sleep(5)

    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    # Пример использования
    m = Main(vacancy='Программист python', salary=300000, only_with_salary=True, role=96)
    if m.auth():
        m.get_links()
        m.response()
        del m
    else:
        del m
