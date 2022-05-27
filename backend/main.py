from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from starlette.templating import _TemplateResponse

from backend.di import DI

app = FastAPI()

app.mount('/static', StaticFiles(directory='templates/static'), name='static')

origins = [
    "*"
]


@app.get('/')
async def index():
    return JSONResponse(status_code=200,
                        content={"status": "OK",
                                 "msg": "Initial"})


@app.get('/page')
async def random(request: Request):
    return DI.templates.TemplateResponse('index.html', {'request': request})

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

