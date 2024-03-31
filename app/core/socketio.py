from socketio import AsyncServer, ASGIApp
# from app.main import app

sio = AsyncServer(async_mode='asgi')

#wrap with ASGI application
socket_app = ASGIApp(sio)

# connect to the redis queue as an external process
# external_sio = socketio.RedisManager('redis://', write_only=True)

# emit an event
# external_sio.emit('my event', data={'foo': 'bar'}, room='my room')