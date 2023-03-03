from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    id: int | None
    descricao: str
    responsavel: str | None
    nivel: int
    situacao: str | None
    prioridade: int

tasks: list[Task] = []

proximo_id = 1

situacao_tarefa = ['NOVA', 'EM ANDAMENTO', 'PENDENTE', 'RESOLVIDA', 'CANCELADA']

# adiciona sempre uma nova tarefa, se ocultar a situação ja seleciona a tarefa como nova.
@app.post('/tarefa', status_code=status.HTTP_201_CREATED)
def adicionar_tarefa(task: Task):
    global proximo_id
    task.id = proximo_id
    task.situacao = situacao_tarefa[0]
    tasks.append(task)
    proximo_id += 1

    return {"status": "success", "data": task}


# lista todas as tarefas ou pode filtrar passando o numero do inicio e fim da busca
@app.get('/tarefa')
def listar_tarefa(skip: int | None = None, take: int | None = None, situacao: str | None = None, nivel: int | None = None, prioridade: int | None = None):
    inicio = skip
    if skip and take:
        fim = skip + take
    else:
        fim = None

    filtro_tarefas = tasks

    if situacao:
        filtro_tarefas = [task for task in filtro_tarefas if task.situacao == situacao]

    if nivel:
        filtro_tarefas = [task for task in filtro_tarefas if task.nivel == nivel]

    if prioridade:
        filtro_tarefas = [task for task in filtro_tarefas if task.prioridade == prioridade]

    return {"status": "success", "data": filtro_tarefas[inicio:fim]}


# listar a tarefa detalhe da tarefa
@app.get('/tarefa/{task_id}')
def detalhes_tarefa(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return {"status": "success", "data": task}
    raise HTTPException(404, detail='Tarefa não existe.')


# deletar tarefa
@app.delete('/tarefa/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(task_id: int):
    for tarefa_atual in tasks:
        if tarefa_atual.id == task_id:
            tasks.remove(tarefa_atual)
            return Response('Sua tarefa foi deletada.')
    raise HTTPException(404, detail='Tarefa não existe.')


# atualizar o status da tarefa
@app.put('/tarefa/{task_id}')
def atualizar_situacao_tarefa(task_id: int, situacao: str):
    for task in tasks:
        if task.id == task_id:
            index = situacao_tarefa.index(situacao.upper())
            if index < situacao_tarefa.index(task.situacao):
                raise HTTPException(400, detail='Não é possível atualizar para um status anterior.')

            task.situacao = situacao.upper()
            return {"status": "success", "data": task}

    raise HTTPException(404, detail='Tarefa não existe.')
