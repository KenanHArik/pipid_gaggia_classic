from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from starlette.websockets import WebSocket, WebSocketState
from starlette.responses import FileResponse
import random
import asyncio
import time

# run this command: uvicorn main:app --reload

app = FastAPI()

'''
Homepage 
'''
@app.get("/")
async def get():
    return FileResponse('static/index.html')

'''
Websocket
'''

@app.websocket_route("/ws")
class WSocket(WebSocketEndpoint):
    sleep = 1
    encoding = None
    
    async def on_connect(self, websocket):
        await websocket.accept()
        # create async tasks here:
        self.task2 = asyncio.create_task(self.give_random(websocket))
    
    async def on_disconnect(self, websocket, close_code):
        self.task2.cancel()
        websocket.application_state = WebSocketState.DISCONNECTED
        assert websocket.client_state == WebSocketState.DISCONNECTED
        print('Websocket Disconnected')

    async def on_receive(self, websocket, data):
        print(f'Received this {data}')

    async def give_random(self, websocket):
        try:
            while websocket.client_state == WebSocketState.CONNECTED:
                rn = (random.random())
                await websocket.send_text(f"Current Temperature is : {rn:.2f} C")
                await asyncio.sleep(self.sleep)
        except Exception as e:
            pass
            # print(f'Exception encountered {e} while sending number')
