import requests
from bs4 import BeautifulSoup


def scrape_movies():
    url = "https://www.kinopoisk.ru/lists/movies/top250/"
    cookies = {
        # с удовольствием оставил свои данные куки, но в целях безопасности их удалил
    }
    response = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = []
    for item in soup.find_all('div', class_='styles_root__ti07r'):

        # Получаем название фильма по названию класса
        title = item.find('span', class_='styles_activeMovieTittle__kJdJj').text

        # Разделяем текст с блока на 2 части, так как в нем объединены режиссер фильма и жанр фильма
        data = item.find('span', class_='desktop-list-main-info_truncatedText__IMQRP').text.split("Режиссёр: ")

        # Получаем режиссёра фильма после разделения
        director = data[-1]

        # Получаем жанр фильма отделение от не нужной информации
        genre = data[0].split(" • ")[-1].strip()

        # Получаем год фильма
        year = int(item.find('span', class_='desktop-list-main-info_secondaryText__M_aus').text.split(", ")[-2])

        # Получаем рейтинг на Кинопоиске
        rating = item.find('span', class_='styles_kinopoiskValue__nkZEC').text

        # Получаем ссылку на постер фильма
        poster_url = item.find('img', class_='styles_mediumSizeType__fPzdD')['src']

        # Проходим по ссылку, получаем содержимое из блока content и сохраняем в формате JPEG в папке image
        r = requests.get(f"https:{str(poster_url)}")
        with open(f"image/{title}.jpg", 'wb') as w:
            w.write(r.content)

        # Записываем полученные данные в список, для дальнейшей работы с ней
        movies.append({"title": title, "director": director, "year": year, "genre": genre, "rating": rating})

    # Так как по данной ссылке у нас только 50 фильмов, а нужно 100, запускаем выгрузку со второй страницы, и объединяем два списка в общий
    movies += open_page(2)

    return movies


def open_page(page):
    # тут всё аналогично как в scrape_movies, только добавилась возможность при вызове фунции присвоить значение страницы

    url = f"https://www.kinopoisk.ru/lists/movies/top250/?page={page}"
    cookies = {
        # с удовольствием оставил свои данные куки, но в целях безопасности их удалил
    }
    response = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies_next_page = []
    for item in soup.find_all('div', class_='styles_root__ti07r'):
        title = item.find('span', class_='styles_activeMovieTittle__kJdJj').text
        data = item.find('span', class_='desktop-list-main-info_truncatedText__IMQRP').get_text().split("Режиссёр: ")
        director = data[-1]
        genre = data[0].split(" • ")[-1].strip()
        year = int(item.find('span', class_='desktop-list-main-info_secondaryText__M_aus').text.split(", ")[-2])
        rating = item.find('span', class_='styles_kinopoiskValue__nkZEC').text
        poster_url = item.find('img', class_='styles_mediumSizeType__fPzdD')['src']
        r = requests.get(f"https:{poster_url}")
        with open(f"image/{title}.jpg", 'wb') as w:
            w.write(r.content)
        movies_next_page.append({"title": title, "director": director, "year": year, "genre": genre, "rating": rating})

    return movies_next_page