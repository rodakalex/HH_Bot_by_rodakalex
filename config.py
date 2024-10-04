import os

login = ''
password = ''


def authenticate():
    global login, password
    import auth
    login = auth.login
    password = auth.password


if os.path.exists('auth.py'):
    authenticate()

else:
    with open('auth.py', 'w') as auth:
        login = input('Введите email\n?> ')
        password = input('Введите пароль\n?> ')
        print('> ')
        auth.write(f"login = '{login}'\npassword = '{password}'")

    authenticate()
