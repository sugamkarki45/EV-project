import socketio

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.on("join_booking")
async def join_booking(sid, data):
    booking_id = data.get("booking_id")
    await sio.enter_room(sid, f"booking:{booking_id}")
