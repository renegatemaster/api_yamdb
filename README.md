# API YaMDb
_API для сервиса YaMDb_  <br><br>
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
## Описание

Этот проект позволяет использовать приложение YaMDb через API: просматривать различные произведения, писать на них отзывы и ставить им оценки.

## Установка

Клонируем репозиторий и переходим в него в командной строке:

```bash
git clone git@github.com:renegatemaster/api_yamdb.git
```

Cоздаём и активируем виртуальное окружение, устанавливаем зависимости:

```bash
python3.9 -m venv venv && \ 
    source venv/bin/activate && \
    python -m pip install --upgrade pip && \
    pip install -r backend/requirements.txt
```

Запускаем проект 

```bash
cd api_yamdb/
python3 manage.py runserver
```

## Прмиеры запросов

#### Регистрация нового пользователя и получение токена: 

На эндпоинт http://127.0.0.1:8000/api/v1/auth/signup/ направляется 
POST-запрос с username и email

```
{
    "email": "example@123.com",
    "username": "examplename"
}
```

На почту приходит код подтверждения, который затем необходимо отправить на адрес
http://127.0.0.1:8000/api/v1/auth/token/ POST-запросом

```
{
    "username": "examplename",
    "confirmation_code": "123"
}
```

В ответ придёт токен

```
{
    "token": "some_token"
}
```

#### Получение произведений

На адрес http://127.0.0.1:8000/api/v1/titles/ направляем GET-запрос

#### Написать отзыв

На адрес http://127.0.0.1:8000/api/v1/titles/{title_id}/review/
направляем POST-запрос с текстом и оценкой

```
{
    "text": "review_text",
    "score": 9
}
```
