from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, Movie, engine
from app.scraper import scrape_movies
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()


def get_db():
    # Dependency для получения сессии базы данных
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Добавляем возможность открыть html файл
app.mount("/static", StaticFiles(directory="static", html=True))

@app.post("/load_movies/")
async def load_movies(db: Session = Depends(get_db)):
    # Запускаем парсер и сохраняем в формате списка
    movies = scrape_movies()

    # Разделяем список на составляющие и записываем в БД
    for movie in movies:
        db_movie = Movie(title=movie['title'], director=movie['director'], year=movie['year'], genre=movie['genre'],
                         rating=movie['rating'])
        db.add(db_movie)
    db.commit()

    # Сортируем фильмы по рейтингу
    sorted_movies = db.query(Movie).order_by(Movie.rating.desc()).all()

    return JSONResponse(content=[
        {"title": movie.title, "director": movie.director, "year": movie.year, "genre": movie.genre,
         "rating": movie.rating} for movie in sorted_movies])