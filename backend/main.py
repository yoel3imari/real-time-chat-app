from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

connections: list[WebSocket] = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        # Load previous messages from Redis
        history = await r.lrange("chat:messages", -50, -1)  # last 50 messages
        for msg in history:
            await websocket.send_text(msg)

        # Listen for new messages
        while True:
            data = await websocket.receive_text()

            # Save message to Redis
            await r.rpush("chat:messages", data)

            # Broadcast to all clients
            for conn in connections:
                await conn.send_text(data)

    except WebSocketDisconnect:
        connections.remove(websocket)
