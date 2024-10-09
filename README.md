# movies_parser
Тестовое задание по написанию парсера с использованием
- Backend: FastAPI | SQLAlchemy.
- SQL: PostgreSQL
- Frontend: jQuery.

После длительного поиска сайта с нужными критериями для каждого фильма, а именно:
- Название фильма
- Режиссёр фильма
- Год выпуска
- Жанр фильма
- Рейтинг фильма
Был подобран сайт kinorium.ru, но после пару запросов, заблокировали доступ к ниму, и пришлось взять сайт от Яндекс, Кинопоиск. Да у него нет официального API, да и не официальный так себе, пришлось воспользоваться функции отправкой куки, которые были полученны с помощью генератора curl, и содержимое сайта было полученно с легкостью.

Структура проекта таковая.
```
movie_parser/
├── app/
│   ├── main.py
│   ├── database.py
│   └── scraper.py
├── templates/
│   └── index.html
├── image/
└── requirements.txt
```

Сам код отвечающий за работе FastAPI сохранен в файле под названием main.py. В которой есть функция для вызова скрапера и строчка кода отвечающая за открытие шаблона страницы index.html.
Для запуска кода нужно вызвать в консоле с проектом 
```
uvicorn app.main:app --reload
```
и запустить сам проект. Ссылка для проверки работоспособности 
```
http://127.0.0.1:8000/static/index.html
```
Скриншоты работа способности кода лежат в папке screenshots
