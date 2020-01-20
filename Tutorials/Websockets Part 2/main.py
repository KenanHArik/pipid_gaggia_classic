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
    encoding = 'text'
    
    async def on_connect(self, websocket):
        await websocket.accept()
        # create asyncronous tasks:
        self.task2 = asyncio.create_task(self.give_random(websocket))
        # self.task1 = asyncio.create_task(self.print_state(websocket))
        # await self.main(websocket)  # awaiting blocking code
    
    async def on_disconnect(self, websocket, close_code):
        self.task2.cancel()
        websocket.application_state = WebSocketState.DISCONNECTED
        assert websocket.client_state == WebSocketState.DISCONNECTED
        # self.task1.cancel()
        # print(websocket.client_state)
        # print(websocket.application_state)
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

    # async def print_state(self, websocket):
    #     while True:
    #         print(f'print client state is {websocket.client_state}')
    #         print(f'print application state is {websocket.application_state}')
    #         await asyncio.sleep(1)
