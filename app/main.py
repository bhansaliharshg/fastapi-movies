import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3, os
from pydantic import BaseModel
from typing import List

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Movie(BaseModel):
    id: int
    title: str
    isAdult: int
    year: int
    runtime: float
    genre: list
    available: int
    rented: int

@app.get('/movies', response_description='Sample Response', response_model=List[Movie])
async def root():
    conn = setup()
    cursor = conn.execute('SELECT * FROM Movie')
    return [convertToMovie(movie) for movie in cursor.fetchall()]

@app.get('/movie/id/{id}', response_description='Retrieve Movie By Id', response_model=Movie)
async def getMovieById(id:str):
    conn = setup()
    query = 'SELECT * FROM Movie where id = ' + id
    cursor = conn.execute(query)
    return convertToMovie(cursor.fetchone())

@app.get('/movie/name/{name}', response_description='Search Movie By Name', response_model=List[Movie])
async def getMovieByName(name: str):
    conn = setup()
    query = 'SELECT * FROM Movie where title LIKE \'%' + name + '%\''
    cursor = conn.execute(query)
    return [convertToMovie(movie) for movie in cursor.fetchall()]

@app.get('/movie/year/{year}', response_description='Search Movie By Year', response_model=List[Movie])
async def getMovieByYear(year: str):
    conn = setup()
    query = 'SELECT * FROM Movie WHERE year = ' + year
    cursor = conn.execute(query)
    return [convertToMovie(movie) for movie in cursor.fetchall()]

@app.get('/movie/genre/{genre}', response_description='Search Movie By Genre', response_model=List[Movie])
async def getMovieByGenre(genre: str):
    conn = setup()
    query = 'SELECT * FROM Movie where genre LIKE \'%' + genre + '%\''
    cursor = conn.execute(query)
    return [convertToMovie(movie) for movie in cursor.fetchall()]

@app.get('/movie/{id}/rent')
async def rentAMovie(id: str):
    conn = setup()
    available, movie = checkIfMovieAvailable(conn, id)
    if available:
        query = 'UPDATE Movie SET rented = ' + str(movie.rented+1) + ', available = ' + str(movie.available-1) + ' WHERE id = ' + id
        cursor = conn.execute(query)
        conn.commit()
        return 'Movie with id:' + id +' rented successfully'
    else:
        return 'Error'

def checkIfMovieAvailable(conn, id: str):
    query = 'SELECT * FROM Movie WHERE id = ' + id
    cursor = conn.execute(query)
    movie = convertToMovie(cursor.fetchone())
    if movie.available > 0 and movie.rented <= 10:
        return True, movie
    return False, movie

def convertToMovie(result):
    return Movie(id=result[0], title=result[1], isAdult=result[2], year=result[3], runtime=result[4], genre=result[5].split(',') if result[5] else [], available=result[6], rented=result[7])

def setup():
    return sqlite3.connect(os.getcwd()+'/assignmenttwo.db')

if __name__ == '__main__':
    uvicorn.run(app)

