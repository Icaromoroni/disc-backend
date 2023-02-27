from fastapi import FastAPI,HTTPException,Response, status
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
situacao_tarefa= ['NOVA', 'EM ANDAMENTO', 'PENDENTE', 'RESOLVIDA', 'CANCELADA']
nivel = [1,3,5,8]
prioridade = [1,2,3]


proximo_id = 1

# funcao para formatar a situacao de uma tarefa para letras maiusculas
def formatação(task: Task):
    s = task.situacao.upper()
    return s


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
def listar_tarefa(skip: int | None = None, take: int | None = None):
    inicio = skip
    if skip and take:
        fim = skip + take
    else:
        fim = None
    return {"status": "success", "data": tasks[inicio:fim]}

# listar a tarefa passando o identificador
@app.get('/tarefa/{task_id}')
def detalhes_tarefa(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return {"status": "success", "data": task}
    raise HTTPException(404, detail='Tarefa não exite.')

# listar tarefas por situação
@app.get('/tarefa/situacao/')
def buscarSituação(situacao: str):
    formatacao = situacao.upper()
    lista = []
    for tarefa in tasks:
        if tarefa.situacao == formatacao:
            lista.append(tarefa)
    if not lista:
        raise HTTPException(status_code=404, detail=f'Não existem tarefas com a situação {formatacao}')
    return {"status": "success", "data": lista}

#listar por nivel
@app.get('/tarefa/nivel/')
def listar_nivel(nivel: int):
    tarefas_nivel = [tarefa for tarefa in tasks if tarefa.nivel == nivel]
    return {"status": "success", "data": tarefas_nivel}
            
#listar por prioridade
@app.get('/tarefa/prioridade/')
def listar_prioridade(p):
    lista = []
    if p in prioridade:
        for tarefa in tasks:
            if tarefa.prioridade == p:
                lista.append(tarefa)
        return {"status": "success", "data": lista}        
    else:
        raise HTTPException(409, detail='Prioridade inválida.')


#  alterar por situação da tarefa
@app.put('/tarefa/{task_id}/{marcar_situacao}')
def marcarSituacao(task_id: int, marcar_situacao: str):
    formatacao = marcar_situacao.upper()
    for marcar_tarefa in tasks:
        if marcar_tarefa.id == task_id:
            if marcar_tarefa.situacao == situacao_tarefa[0]:
                if formatacao == situacao_tarefa[1]:
                    marcar_tarefa.situacao = formatacao
                    tasks[task_id - 1] = marcar_tarefa
                    return {"status": "success", "data": marcar_tarefa}
                elif formatacao == situacao_tarefa[2]:
                    marcar_tarefa.situacao = formatacao
                    tasks[task_id - 1] = marcar_tarefa
                    return {"status": "success", "data": marcar_tarefa}
                elif formatacao == situacao_tarefa[4]:
                    marcar_tarefa.situacao = formatacao
                    tasks[task_id - 1] = marcar_tarefa
                    return {"status": "success", "data": marcar_tarefa}
            elif marcar_tarefa.situacao == situacao_tarefa[1]:
                if formatacao == situacao_tarefa[2]:
                    marcar_tarefa.situacao = formatacao
                    tasks[task_id - 1] = marcar_tarefa
                    return {"status": "success", "data": marcar_tarefa}
                elif formatacao == situacao_tarefa[3]:
                    marcar_tarefa.situacao = formatacao
                    tasks[task_id - 1] = marcar_tarefa
                    return {"status": "success", "data": marcar_tarefa}
                elif formatacao == situacao_tarefa[4]:
                    tasks[task_id - 1] = marcar_tarefa
                    return {"status": "success", "data": marcar_tarefa}
            elif marcar_tarefa.situacao == situacao_tarefa[2]:
                if formatacao == situacao_tarefa[1]:
                    marcar_tarefa.situacao = formatacao
                    tasks[task_id - 1] = marcar_tarefa
                    return {"status": "success", "data": marcar_tarefa}
                elif formatacao == situacao_tarefa[4]:
                    tasks[task_id - 1] = marcar_tarefa
                    return {"status": "success", "data": marcar_tarefa}
    raise HTTPException(409, detail='Sua tarefa esta com a situacao escolhida, vazia ou com o ciclo avancado.')


# alterar qualquer tarefa da tarefa menos as canceladas
@app.put('/tarefa/{task_id}')
def alterar_tarefa(task_id: int, task: Task):
    if task_id > 0 or task_id == None:
        task.id = task_id
        for tarefa in tasks:
            if tarefa.id == task_id:
                if tarefa.situacao != situacao_tarefa[4]:
                    task.situacao = formatação(task)
                    tasks[task_id - 1] = task
                    return Response('Sua alterção foi realizada.')
                else:
                    raise HTTPException(409, detail= 'Você não pode alterar uma tarefa cancelada.')
    else:
        raise HTTPException(409, detail= 'Identificador invalido')


# deletar tarefa
@app.delete('/tarefa/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(task_id: int):
    for tarefa_atual in tasks:
        if tarefa_atual.id == task_id:
            tasks.remove(tarefa_atual)
            return Response('Sua tarefa foi deletada.')
    raise HTTPException(404, detail='Tarefa não exite.')

