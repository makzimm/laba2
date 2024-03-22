#Импортируем необходимые модули и создадим инстанс FastAPI
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
import pyjokes
import wikipediaapi

# Установим язык для wikipedia РУ
wiki_wiki = wikipediaapi.Wikipedia('127.0.0.1', 'ru')

#Определим Pydantic модели для запросов и ответов:
class WikiQueryParams(BaseModel):
        query: str

class WikiBodyParams(BaseModel):
        query: str

class WikiResponse(BaseModel):
        title: str
        pageid: int
        summary: str

#Создадим роуты в соответствии с заданием:
app = FastAPI()

#GET /path/{title} получает данные страницы Wikipedia по заголовку.
@app.get("/path/{title}", response_model=WikiResponse)
def get_wiki_by_path(title: str):
        page = wiki_wiki.page(title)
        if not page.exists():
                raise HTTPException(status_code=404, detail="Page not found")
        return {
                "title": page.title,
                "pageid": page.pageid,
                "summary": page.summary
        }

#GET /query/ использует query параметр для извлечения данных страницы Wikipedia.
@app.get("/query/", response_model=WikiResponse)
def get_wiki_by_query(query: str):
       page = wiki_wiki.page(query)
       if not page.exists():
           raise HTTPException(status_code=404, detail="Content not found")
       return {
           "title": page.title,
           "pageid": page.pageid,
           "summary": page.summary
       }

#POST /body/ получает данные страницы Wikipedia через тело запроса в формате JSON.
@app.post("/body/", response_model=WikiResponse)
def get_wiki_by_body(params: WikiBodyParams = Body(...)):
        page = wiki_wiki.page(params.query)
        if not page.exists():
                raise HTTPException(status_code=404, detail="Content not found")
        return {
                "title": page.title,
                "pageid": page.pageid,
                "summary": page.summary
        }