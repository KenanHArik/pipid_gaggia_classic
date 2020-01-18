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
# declare global loop


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
    rate = 1
    encoding = "text"
    
    async def on_disconnect(self, websocket, close_code):
        print(f'Loop is stopped at: {time.strftime("%M:%S", time.localtime())}')
        # loop.stop()
        await websocket.close()
        print(f'Loop is stopped at: {time.strftime("%M:%S", time.localtime())}')
    
    async def on_connect(self, websocket):
        await websocket.accept()
        await self.main(websocket)

    async def main(self, websocket):
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        responses = {}
        url = "https://apress.com"
        await asyncio.gather(self.fetch(websocket, fut=future), websocket.receive_text(), self.give_random(websocket, self.rate))
   
    async def fetch(self, websocket, fut: asyncio.Future):
        msg = await websocket.receive_text()
        fut.set_result(msg)

    async def checker(self, websocket, fut: asyncio.Future):
        result = await fut
        print(result)
    
    async def give_random(self, websocket, rate):
        while True:
            rn = (random.random())
            await websocket.send_text(f"Current Temperature is : {rn:.2f} C")
            await asyncio.sleep(rate)



