from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from starlette.responses import FileResponse
import random
import asyncio


# run this command: uvicorn main:app --reload
async def infinite_random():
    while True:
        yield random.random()
        await asyncio.sleep(3)


def infinite_random2():
    while True:
        yield random.random()


app = FastAPI()


@app.get("/")
async def get():
    return FileResponse('static/index.html')


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    async def get_message(websocket):
        while True:
            text = await websocket.receive_text()
            await websocket.send_text(f"Received Text is: {text}")

    async def give_random(websocket):
        while True:
            rn = next(infinite_random2())
            await asyncio.sleep(1)
            await websocket.send_text(f"Random Number is : {rn}")

    async def handler(websocket):
        msg_task = asyncio.ensure_future(get_message(websocket))
        rn_task = asyncio.ensure_future(give_random(websocket))
        done, pending = await asyncio.wait(
            [msg_task, rn_task], return_when=asyncio.FIRST_COMPLETED
        )
        print(done)
        for task in pending:
            task.cancel()

    while True:
        # How to get recieve while sending is going?!? See:
        # https://websockets.readthedocs.io/en/stable/intro.html
        await handler(websocket)