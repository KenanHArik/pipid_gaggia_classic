from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from starlette.websockets import WebSocket
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
        await self.main(websocket)  # awaiting blocking code
    
    async def on_disconnect(self, websocket, close_code):
        print('Websocket Disconnected')

    async def main(self, websocket):
        try:
            task2 = asyncio.create_task(self.give_random(websocket))
            task1 = asyncio.create_task(self.get_message(websocket))
            while True:
                await asyncio.sleep(100) # blocking function to stay in try loop
        except Exception as e:
            print(f'Exception was {e}')
            print(f'Attempting to cancel tasks')
            try:
                task1.cancel()
            except:
                print(f'Exception encounterd canceling Task1')
            try:
                task2.cancel()
            except:
                print(f'Exception encounterd canceling Task2')

    async def get_message(self, websocket):
        while True:
            try:
                data = await websocket.receive_text()
                print(f'Received this {data}')
            except:
                print('Socket Receive exception')
                break

    async def give_random(self, websocket):
        while True:
            try:
                rn = (random.random())
                await websocket.send_text(f"Current Temperature is : {rn:.2f} C")
                await asyncio.sleep(self.sleep)      
            except:
                print('Exception encountered while sending number')
                break