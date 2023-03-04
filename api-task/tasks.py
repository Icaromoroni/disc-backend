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

# remover tarefa
@app.delete('/tarefa/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def remover_tarefa(task_id: int):
    for tarefa_atual in tasks:
        if tarefa_atual.id == task_id:
            tasks.remove(tarefa_atual)
            return Response('Sua tarefa foi deletada.')
    raise HTTPException(404, detail='Tarefa não existe.')


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
        filtro_tarefas = [task for task in filtro_tarefas if task.situacao == situacao.upper()]

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


# atualizar o status da tarefa
@app.put('/tarefa/{task_id}')
def atualizar_situacao_tarefa(task_id: int, situacao: str | None = None, task: Task | None = None):
    if task != None:
        formatacao = task.situacao.upper()
        print(formatacao)
        for index in range(1,len(tasks)):
            tarefa = tasks[index]
            if tarefa.id == task_id:
                task.id = tarefa.id
                task.situacao = formatacao
                if task.situacao in situacao_tarefa:
                    tasks[index] = task
                    return task
                else:
                    raise HTTPException(400, detail='Situação inválida')
    else:
        for task in tasks:
            if task.id == task_id:
                index = situacao_tarefa.index(situacao.upper())

                if situacao_tarefa.index(task.situacao) == 3 or situacao_tarefa.index(task.situacao) == 4:
                    raise HTTPException(400, detail=f'Não é posível alterar tarefa {task.situacao}')            
                elif index == 4:
                    task.situacao = situacao.upper()
                    return {"status": "success", "data": task}
                elif index == 1 or index == 2:
                    task.situacao = situacao.upper()
                    return {"status": "success", "data": task}
                elif index == 3 and situacao_tarefa.index(task.situacao) != 2 and situacao_tarefa.index(task.situacao) != 0:
                    task.situacao = situacao.upper()
                    return {"status": "success", "data": task}
                else:
                    raise HTTPException(400, detail=f'Não é posível pular a tarefa da situação >{task.situacao}< para >{situacao.upper()}<!')

        raise HTTPException(404, detail='Tarefa não existe.')
