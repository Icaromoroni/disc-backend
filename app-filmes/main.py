
from fastapi import FastAPI, HTTPException,Response,status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['http://127.0.0.1:5500',
           'http://127.0.0.1:8000']
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

class Filme(BaseModel):
    id: int | None
    nome: str
    genero:str
    ano: int
    duracao: int

filmes: list[Filme] = []

'''for i in range(10):
    filme = Filme(id=100+i,
                  nome='titanic',
                  genero='Romance',
                  ano=1997,
                  duracao=150
                  )
    filmes.append(filme)'''


@app.get("/filmes")
def todos_filmes(skip: int | None = None, take: int | None = None):
    inicio = skip
    if skip and take:
        fim = skip + take
    else:
        fim = None

    return filmes[inicio:fim]


@app.get('/filmes/{filme_id}')
def obter_filme(filme_id:int):
    for filme in filmes:
        if filme.id == filme_id:
            return filme
    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail=f'Não há filme com id ={filme_id}')

@app.post('/filmes', status_code=status.HTTP_201_CREATED)
def novo_filme(filme: Filme):
    filme.id = len(filmes) + 1
    filmes.append(filme)

    return filme

@app.delete('/filmes/{filme_id}', status_code=status.HTTP_204_NO_CONTENT)
def deletar_filme(filme_id: int):
    for filme_atual in filmes:
        if filme_atual.id == filme_id:
            filmes.remove(filme_atual)
            return {'Deletado'}

    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail=f'Não há filme com id ={filme_id}')

@app.put('/filmes/{filme_id}')
def atualizar_filme(filme_id: int, filme: Filme):
    for index in range(len(filmes)):
        filme_atual = filmes[index]
        if filme_atual.id == filme_id:
            filme.id = filme_atual.id
            filmes[index] = filme
            return filme

    raise HTTPException(404,detail = "Filme não encontrado")
