from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from starlette.websockets import WebSocket
from starlette.responses import FileResponse
import random
import asyncio


# run this command: uvicorn main:app --reload


app = FastAPI()


# async def socket_loop():
#     data = await websocket.receive_text()
#     if data:
#         print(data)
#     temp = random.random()
#     print(temp)
#     await websocket.send_text(str(temp))
#     await asyncio.sleep(0.5)
    # divs1 = loop.create_task(find_divisibles(508000, 34113))
    # divs2 = loop.create_task(find_divisibles(100052, 3210))
    # divs3 = loop.create_task(find_divisibles(500, 3))
    # await asyncio.wait([divs1,divs2,divs3])
    # return divs1, divs2, divs3

async def send_random():
    while True:
        random.random()
        asyncio.sleep(1)
        await rn


@app.get("/")
async def get():
    return FileResponse('static/index.html')


@app.websocket_route("/ws")
class WSocket(WebSocketEndpoint):
    counter = 0
    encoding = "text"
    
    async def on_disconnect(self, websocket, close_code):
        loop.close()
        websocket.close()
        pass
    
    async def on_connect(self, websocket):
        await websocket.accept()
        # while True:
        #     await self.handler(websocket)
        #
        # loop = asyncio.get_event_loop()
        # loop.create_future()
        # loop.create_task(self.give_random(websocket))
        # loop.create_task(self.get_message(websocket))
        # loop.run_forever()
        # #
        # https://docs.python.org/3/library/asyncio-eventloop.html#running-and-stopping-the-loop
        # await asyncio.sleep(3)
        asyncio.ensure_future(self.give_random(websocket))
        asyncio.ensure_future(self.get_message(websocket))
        # loop.run_until_complete()
        # loop.run_forever()
#     except:
        
        while True:
            await self.handler(websocket)

    async def get_message(self, websocket):
        while True:
            text = await websocket.receive_text()
            print(text)
            # await websocket.send_text(f"Received Text is: {text}")

    def infinite_random2(self):
        while True:
            yield random.random()

    async def give_random(self, websocket):
        while True:
            rn = next(self.infinite_random2())
            await asyncio.sleep(1)
            await websocket.send_text(f"Current Temperature is : {rn:.2f} C")

    async def handler(self, websocket):
        msg_task = asyncio.ensure_future(self.get_message(websocket))
        rn_task = asyncio.ensure_future(self.give_random(websocket))
        done, pending = await asyncio.wait(
            [msg_task, rn_task], return_when=asyncio.FIRST_COMPLETED
        )
        print(done)
        for task in pending:
            task.cancel()

    

# @app.websocket_route("/ws")
# class WSocket(WebSocketEndpoint):
#     counter = 0
#     encoding = "text"
    
#     async def on_disconnect(self, websocket, close_code):
#         websocket.close()
#         pass
    
#     async def on_connect(self, websocket):
#         await websocket.accept()
#         while True:
#             await self.handler(websocket)

#     async def get_message(self, websocket):
#         while True:
#             text = await websocket.receive_text()
#             print(text)
#             # await websocket.send_text(f"Received Text is: {text}")

#     def infinite_random2(self):
#         while True:
#             yield random.random()

#     async def give_random(self, websocket):
#         while True:
#             rn = next(self.infinite_random2())
#             await asyncio.sleep(1)
#             await websocket.send_text(f"Current Temperature is : {rn:.2f} C")

#     async def handler(self, websocket):
#         msg_task = asyncio.ensure_future(self.get_message(websocket))
#         rn_task = asyncio.ensure_future(self.give_random(websocket))
#         done, pending = await asyncio.wait(
#             [msg_task, rn_task], return_when=asyncio.FIRST_COMPLETED
#         )
#         print(done)
#         for task in pending:
#             task.cancel()





# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     # loop = asyncio.get_event_loop()
#     try:
#         # while True:
#             # data = await websocket.receive_text()
#             # if data:
#             #     print(data)
#             # await websocket.send_text(str(random.random()))
#             # await asyncio.sleep(1)
#         consumer_task = asyncio.ensure_future(await websocket.receive_text())
#         producer_task = asyncio.ensure_future(await send_random())
#         done, pending = await asyncio.wait([consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED)
#         for task in pending:
#             task.cancel()
#             # loop.create_future()
#             # f.add_done_callback(lambda x: print(x))
#             # if data:
#             #     print(data)
#             # loop.create_task()
#             # loop.create_task(await asyncio.sleep(1))
#             # loop.run_until_complete()
#     except:
#         # need to log here
#         pass
#     finally:
#         # loop.close()
#         await websocket.close()

