from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

active_connections = set()
app = FastAPI()

class Load(BaseModel) : 
    name : str
    price : float 
    is_offer : bool | None = None

@app.websocket("/draw")
async def websocket_endpoint(websocket : WebSocket) :
    await websocket.accept()
    active_connections.add(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Websocket {websocket} has connected")
            #### TODO A FOR CYCLE TO SEND EVERYBODY INFO

    except WebSocketDisconnect :
        print(f"Websocket {websocket} has disconnected.")
        