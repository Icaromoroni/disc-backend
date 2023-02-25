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
s= ['NOVA', 'EM ANDAMENTO', 'PENDENTE', 'RESOVIDA', 'CANCELADA']
nivel = [1,3,5,8]
prioridade = [1,2,3]

def formatação(task: Task):
    s = task.situacao.upper()
    return s
    


@app.post('/tarefa', status_code=status.HTTP_201_CREATED)
def adicionar_tarefa(task: Task):
    task.id = len(tasks) + 1
    task.situacao = s[0]
    tasks.append(task)
    return task

@app.get('/tarefa')
def listar_tarefa(skip: int | None = None, take: int | None = None):
    inicio = skip
    if skip and take:
        fim = skip + take
    else:
        fim = None
    return tasks[inicio:fim]

@app.get('/tarefa/{task_id}')
def detalhes_tarefa(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    
    raise HTTPException(404, detail='Tarefa não exite.')


'''@app.get('/tarefa/')
def buscarSituação(situacao):
    if situacao:
        for procurar_situacao in tasks:
            print(procurar_situacao)
            if procurar_situacao.situacao == situacao:
                procurar_situacao += procurar_situacao
                return procurar_situacao

    pass'''


#alterar qualquer item da tarefa menos as canceladas
@app.put('/tarefa/{task_id}')
def alterar_tarefa(task_id: int, task: Task):
    if task_id > 0 or task_id == None:
        task.id = task_id
        for tarefa in tasks:
            if tarefa.id == task_id:
                if tarefa.situacao != s[4]:
                    task.situacao = formatação(task)
                    tasks[task_id - 1] = task
                    return Response('Sua alterção foi realizada.')
                else:
                    raise HTTPException(409, detail= 'Você não pode alterar uma tarefa cancelada.')
    else:
        raise HTTPException(409, detail= 'Identificador invalido')


@app.delete('/tarefa/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(task_id: int):
    for tarefa_atual in tasks:
        if tarefa_atual.id == task_id:
            tasks.remove(tarefa_atual)
            return Response('Deletado com sucesso')
    raise HTTPException(404, detail='Tarefa não exite.')

