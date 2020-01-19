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

    # async def on_receive(self, websocket, data):
    #     print(data)
        # await websocket.send_text(f"Message text was: {data}")
    
    async def on_connect(self, websocket):
        await websocket.accept()
        await self.main(websocket)  # awaiting blocking code
    
    async def on_disconnect(self, websocket, close_code):
        print('Websocket Disconnected')

    async def main(self, websocket):
        # while True:
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






'''
Reference impolimentation

await websocket.accept()
    try:
        task2 = asyncio.create_task(give_random(websocket, 1))
        task1 = asyncio.create_task(get_message(websocket))
        while True:
            await asyncio.sleep(100) # blocking function to stay in try loop
    except Exception as e:
        print(f'Exception was {e}')
        print(f'Attempting to cancel tasks')
        try:
            task1.cancel()
            print('Cancelled Task1')
        except:
            print('Uh oh - task 1 cancel exception')
        try:
            task2.cancel()
            print('Cancelled Task2')
        except:
            print('Uh oh - task 2 cancel exception')

async def get_message(websocket):
    while True:
        data = await websocket.receive_text()
        print(data)

async def give_random(websocket, rate):
    while True:
        try:
            rn = (random.random())
            await websocket.send_text(f"Current Temperature is : {rn:.2f} C")
            await asyncio.sleep(rate)
        except:
            print('Got an error sending a number')
            break

'''







'''
Class implimentation - returns error at close - need to investigate

'''

# class WSocket(WebSocketEndpoint):
#     sleep = 1
#     encoding = 'text'

#     async def on_receive(self, websocket, data):
#         pass
#         # await websocket.send_text(f"Message text was: {data}")
    
#     async def on_connect(self, websocket):
#         await websocket.accept()
#         await self.main(websocket)  # awaiting blocking code
    
#     async def on_disconnect(self, websocket, close_code):
#         print('Websocket Disconnected')

#     async def main(self, websocket):
#         # while True:
#         loop = asyncio.get_event_loop()
#         try:
#             task1 = loop.create_task(self.get_message(websocket), )
#             task2 = loop.create_task(self.give_random(websocket))
#             await asyncio.gather(task1, task2, return_exceptions=True)  # blocking code
#         except Exception as e:
#             print(f'Exception was {e}')
#             print(f'Attempting to cancel tasks')
#             try:
#                 task1.cancel()
#             except:
#                 print(f'Exception encounterd canceling Task1')
#             try:
#                 task2.cancel()
#             except:
#                 print(f'Exception encounterd canceling Task2')

#     async def get_message(self, websocket):
#         while True:
#             try:
#                 data = await websocket.receive_text()
#                 print(f'Received this {data}')
#             except:
#                 print('Socket Receive exception')
#                 break

#     async def give_random(self, websocket):
#         while True:
#             try:
#                 rn = (random.random())
#                 await websocket.send_text(f"Current Temperature is : {rn:.2f} C")
#                 await asyncio.sleep(self.sleep)      
#             except:
#                 print('Exception encountered while sending number')
#                 break


# '''

# With using gather - may run into memory issue on keeping return?!?!
# '''


# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     loop = asyncio.get_event_loop()
#     try:
#         print('before task')
#         task2 = loop.create_task(give_random(websocket, 1))
#         task1 = loop.create_task(get_message(websocket))
#         print('after task forever')
#         # await asyncio.gather(task1, task2)
#         await asyncio.gather(task1, task2)  # blocking code
#         # loop.run_forever()
#     except Exception as e:
#         print(f'Exception was {e}')
#         print(f'Attempting to cancel tasks')
#         try:
#             task1.cancel()
#         except:
#             print('task 1 cancel exception')
#         try:
#             task2.cancel()
#         except:
#             print('task 2 cancel exception')


# async def get_message(websocket):
#     while True:
#         data = await websocket.receive_text()
#         print(data)

# async def give_random(websocket, rate):
#     while True:
#         try:
#             rn = (random.random())
#             await websocket.send_text(f"Current Temperature is : {rn:.2f} C")
#             await asyncio.sleep(rate)
#         except:
#             print('Got an error sending a number')
#             break

