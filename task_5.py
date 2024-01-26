# Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание. Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).

# API должен содержать следующие конечные точки:
# — GET /tasks — возвращает список всех задач.
# — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
# — POST /tasks — добавляет новую задачу.
# — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
# — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.

# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. Для этого использовать библиотеку Pydantic.

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional
from pydantic import BaseModel
import pandas as pd

app = FastAPI()
tasks = []

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: Optional[str] = None


@app.get('/tasks/', response_class=HTMLResponse)
async def show_tasks():
    tasks_table = pd.DataFrame([vars(task) for task in tasks]).to_html()
    return tasks_table

@app.get ('/tasks/{task_id}', response_class=HTMLResponse)
async def show_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task = pd.DataFrame(task).to_html()
            return task
        messedge = "Вы ошиблись, такой задачи нет"
        return JSONResponse(content=messedge, status_code=200)

@app.post ('/tasks', response_class=JSONResponse)
async def create_tasks(task:Task):
    task.id = len(tasks) + 1
    tasks.append(task)
    messedge = "Задача успешно добавлена в список задач"
    return JSONResponse(content=messedge, status_code=200)


@app.put('/tasks/{task_id}', response_class=JSONResponse)
async def change_task(task_id: int, new_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            new_task.id = task.id 
            tasks[index] = new_task
            messedge = "Список задач успешно отредактирован"
            return JSONResponse(content=messedge, status_code=200)
        messedge = "Вы ошиблись, такой задачи нет"
        return JSONResponse(content=messedge, status_code=200)



@app.delete('/tasks/{task_id}')
async def del_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            messedge = 'Задача успешно удалена'
            return JSONResponse(content=messedge, status_code=200)
        messedge = "Вы ошиблись, такой задачи нет"
        return JSONResponse(content=messedge, status_code=200)