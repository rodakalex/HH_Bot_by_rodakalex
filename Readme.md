Вот `README.md` на русском языке для вашего проекта:


# JobAutomation Bot

Python-бот для автоматизации подачи заявок на вакансии на сайте hh.ru. Этот бот выполняет аутентификацию с использованием учетных данных, собирает ссылки на вакансии и подает заявки, основываясь на указанном резюме.

## Содержание
- [Требования](#требования)
- [Установка](#установка)
- [Конфигурация](#конфигурация)
- [Использование](#использование)
- [Функции](#функции)
- [Примечания](#примечания)
- [Отказ от ответственности](#отказ-от-ответственности)

## Требования

- Python 3.x
- Selenium
- Edge WebDriver
- Файл `config.py` с учетными данными и названием резюме

## Установка

1. Установите необходимые пакеты:

 ```
    pip install -r requirements.txt
```

2. Скачайте [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/), совместимый с вашей версией браузера, и добавьте его в переменную PATH системы.

3. Создайте файл `config.py` в директории проекта со следующей структурой:

   ```python
   login = "ваш_логин@example.com"
   password = "ваш_пароль"
   base_url = "https://hh.ru/search/vacancy?text=Ваш_Запрос"
   job = "Название Резюме"
   ```

## Использование

1. Запустите скрипт:

   ```bash
   python main.py
   ```

2. Бот будет выполнять следующие действия:
   - Вход на hh.ru с использованием ваших учетных данных.
   - Сбор ссылок на вакансии по заданному поисковому запросу.
   - Подача откликов на каждую найденную вакансию с использованием указанного резюме.

## Функции

- **Аутентификация**: Выполняет вход в систему с использованием учетных данных на hh.ru.
- **Сбор ссылок на вакансии**: Получает URL вакансий со страниц поиска.
- **Автоматическая подача откликов**: Подает заявки на сохраненные вакансии.
- **Сохранение cookies**: Сохраняет сессионные cookies, чтобы избежать повторной аутентификации.

## Примечания

- Убедитесь, что `config.py` содержит корректные учетные данные.
- Интерфейс hh.ru может меняться, поэтому скрипт может потребовать адаптации.