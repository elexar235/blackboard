from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ValidationError
import json

active_connections = set()
app = FastAPI()

# Pydantic class to validate draw payload
class PayloadDraw(BaseModel) : 
    x : float
    y : float
    pressure: float

# Pydantic class to validate picture payload
class PayloadPicture(BaseModel):
    x : float
    y : float
    image_data : str

@app.websocket("/draw")
async def websocket_endpoint(websocket : WebSocket) :
    await websocket.accept() # websocket handshake
    active_connections.add(websocket) # add a connection to the set
    print(f"Websocket {websocket} has connected")

    # try in case a client disconnects
    try:
        while True: # infinite loop so that a websocket would update every client
            data = await websocket.receive_text()

            # try in case an invalid payload comes
            try:
                data_dict = json.loads(data)
                action = data_dict.get("action")
                payload = data_dict.get("data")
                if action == "draw":
                    # Validate the payload using pydantic
                    try: 
                        validated_draw = PayloadDraw.model_validate(payload)
                        # Send the payload to all active connections
                        for client in active_connections:
                            if client == websocket: 
                                continue
                            await client.send_text(data)

                    except ValidationError as e:
                        print(f"Mistake in format of draw coordinates: {e}")

                elif action == "picture":
                    # Validate the payload using pydantic
                    try: 
                        validated_picture = PayloadPicture.model_validate(payload)
                        # Send the payload to all active connections
                        for client in active_connections:
                            if client == websocket: 
                                continue
                            await client.send_text(data)

                    except ValidationError as e:
                        print(f"Mistake in picture format {e}")

            except json.JSONDecodeError:
                print("Invalid JSON text")


    except WebSocketDisconnect :
        print(f"Websocket {websocket} has disconnected.")
        