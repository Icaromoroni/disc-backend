from fastapi import FastAPI,HTTPException,Response, status
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    id: int
    descricao: str
    responsavel: str | None
    nivel: int
    situacao: str | None
    prioridade: int

tasks: list[Task] = []
situacao = ['NOVA', 'EM ANDAMENTO', 'PENDENTE', 'RESOVIDA', 'CANCELADA']
nivel = [1,3,5,8]
prioridade = [1,2,3]


@app.post('/tarefa', status_code=status.HTTP_201_CREATED)
def adicionar_tarefa(task: Task):
    task.id = len(tasks) + 1
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

@app.put('/tarefa/{task_id}')
def alterar_tarefa(task_id: int, task: Task):
    if task_id > 0:
        for tarefa in tasks:
            if tarefa.id == task_id:
                print(tarefa)
                tasks[task_id - 1] = task
                return Response('Sua alterção foi realizada.')
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail= 'Identificador invalido')

def alterarSituação(task_id: int, situacao: str):
    pass


@app.delete('/tarefa/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(task_id: int):
    for tarefa_atual in tasks:
        if tarefa_atual.id == task_id:
            tasks.remove(tarefa_atual)
            return Response('Deletado com sucesso')
    raise HTTPException(404, detail='Tarefa não exite.')


