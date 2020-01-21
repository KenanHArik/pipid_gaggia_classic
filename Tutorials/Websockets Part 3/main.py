# from fastapi import FastAPI
from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from starlette.websockets import WebSocket, WebSocketState
from starlette.responses import FileResponse
from starlette.routing import Route, WebSocketRoute
import uvicorn
import random
import asyncio
import time

'''
Homepage 
'''

class Homepage(HTTPEndpoint):
    async def get(self, request):
        return FileResponse('static/index.html')

'''
Websocket
'''

class WSocket(WebSocketEndpoint):
    ''' Class for controlling Espresso Machine Control over Websockets
    '''
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
                await websocket.send_text(f"Current Temperature is {z}: {rn:.2f} C")
                await asyncio.sleep(self.sleep)
        except Exception as e:
            raise e from None
            # print(f'Exception encountered {e} while sending number')

'''
app startup and configuration
'''

async def app_startup():
    print(z)
    print('Starting up Starlette')
    await asyncio.sleep(1)

async def app_shutdown():
    print('Shutting down Starlette')
    await asyncio.sleep(1)

z=5
routes = [Route("/", Homepage), WebSocketRoute("/ws", WSocket)]
app = Starlette(routes=routes, on_startup=[app_startup], on_shutdown=[app_shutdown])

'''
main
'''

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
    # run this command: uvicorn main:app --reload

