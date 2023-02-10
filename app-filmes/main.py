from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()


class Filme(BaseModel):
    id: int | None
    nome: str
    genero: str
    ano: int
    duracao: int

filmes: list[Filme] = []

for i in range(10):
    filme = Filme(
                id=100+1,
                nome='Titanic',
                genero='Romance',
                ano=1997,
                duracao=150)
    filmes.append(filme)

@app.get('/filmes')
def todos_filmes(skip: int | None = None, take: int | None = None):
    inicio = skip

    if skip and take:
        fim = skip + take
    else:
        fim = None
    
    return filmes[inicio:fim]