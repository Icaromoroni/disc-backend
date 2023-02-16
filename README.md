Recurso: Filme (filmes)
EndPoints
baseURL: http://127.0.0.1:8000

METHOD     URL           PAYLOAD   DESCRIPTION

GET        /filmes       False     all
GET        /filmes/123   False     One
POST       /filmes       True      Create Resource
DELETE     /filmes/123   False     Delete One(123)
PUT        /filmes/123   True      Update One(123)
PATCH      /filmes/123   True      Partial Update One(123)
