Math app
===============

Math app - это образовательно веб-приложение для подготовки к ОГЭ по математике. Благодаря ему можно ознакомиться со структурой экзамена и потренироваться в решении задач.

На данный момент приложение находится на этапе разработки.

![Start page](screenshots/main_page.png?raw=true "Start page")

Технологии
----------------
### Backend

- SQLite3
- Django4

### Frontend

- JavaScript
- Boostrap
- CKEditor


Функционал
----------------
* Пользователь может решить готовый вариант или составить вариант из тестов необходимых категорий.
![Select tests](screenshots/select_tests.png?raw=true "Select tests")
* Набор тестов в выбранных пользователем категориях рандомизирован.
* Время выполнения варианта записывается, таймер запускается сразу после начала экзамена.
* В зависимости от категорий пользователь отвечает на вопросы с выбором варианта ответа или с развернутым ответом.
* Ответы незарегистрированных пользователей сохраняются в сессию и экзамен может быть завершен в любое время, пока время жизни сессии не истекло.
* Ответы зарегистрированных пользователей сохраняются в базе данных и статистика по выполненным экзаменам доступна из профиля пользователя
![Exam](screenshots/exam.png?raw=true "Exam")  
* После завершения экзамена пользователь попадает на страницу прогресса, на которой отражена статистика верных и неверных ответов.
* Для каждого экзамена установлены проходные балы в соответствие со спецификацией ОГЭ.
![Result page](screenshots/result.png?raw=true "Result")
* После регистрации и авторизации результаты экзамена пользователя будут сохранены в базу данных и доступно во вкладке статистика в профиле или в навигационном меню.
![Statistics page](screenshots/statistics.png?raw=true "Statistics")
* Для пользователей доступны регистрация, авторизация, смена пароля, восстановление пароля через указанный email, редактирование профиля.
![Authorization page](screenshots/authorization.png?raw=true "Authorization")
![Registration page](screenshots/registration.png?raw=true "Registration")
* Реализован удобный интерфейс для пополнения базы данных тестов с математическими формулами.
![Admin panel](https://i.imgur.com/o3nxhAp.png "Admin interface")


Установка
------------
Клонируйте репозиторий:

```git clone https://github.com/ekzanoskina/math_app.git``

Cоздайте виртуальное окружение:

```python -m venv venv```

Убедитесь, что находитесь в директории math_app/ либо перейдите в неё:

```cd math_app```

Активируйте виртуальное окружение:

Для Mac:
 
```source venv/bin/activate```

Для Windows:

```source venv/Scripts/activate```

При необходимости обновите pip:

```pip install --upgrade pip```

Установите зависимости из файла requirements.txt:

```pip install -r requirements.txt```

Из соображений безопасности секретный ключ и пароль от почты для восстановления пароля хранится в файле .env В репозитории необходимо создать файл '.env' и заполнить его по шаблону:

```
SECRET_KEY='<your_secret_key>'
DEBUG=False
EMAIL_HOST_USER = "<your_email>@yandex.ru"
EMAIL_HOST_PASSWORD = '<your_email_password>'
SOCIAL_AUTH_GITHUB_SECRET = ''
SOCIAL_AUTH_GITHUB_KEY = ''
```
Запустите программу
```
python manage.py runserver
```

Использование
------------
Проект задеплоен на бесперебойно работающий сервер PythonAnywhere. 
Ссылка на проект https://zanoskina.pythonanywhere.com

