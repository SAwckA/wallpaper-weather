import asyncio
import random

from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from starlette.templating import _TemplateResponse

from websockets.exceptions import ConnectionClosedOK

from backend.di import DI
from backend.services.weatherbit_weather import get_weather_by_coords, Coords, Weather


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


@app.get('/wallpaper')
async def random(request: Request):
    return DI.templates.TemplateResponse('index.html', {'request': request})


@app.get('/getWeather', response_model=Weather) # 43.026257, 131.887430
async def get_weather(request: Request, altitude: float = 43.026257, longitude: float = 131.887430) -> Weather:
    return get_weather_by_coords(Coords(altitude=altitude, longitude=longitude))


@app.websocket("/ws")
async def websocket_enpoint(websocket: WebSocket, altitude: float = 43.026257, longitude: float = 131.887430):
    await websocket.accept()
    while True:
        response = await websocket.receive()
        if response.get('text') == 'OPEN' or response.get('text') == 'OK':
            data = get_weather_by_coords(Coords(altitude=altitude, longitude=longitude))
            await websocket.send_text(data.json())
            await asyncio.sleep(5)
        else:
            await websocket.close()

@app.exception_handler(ConnectionClosedOK)
async def ws_connection_closed_ok(request, exc):
    return None


app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

