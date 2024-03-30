from main import app
from fastapi_socketio import SocketManager

socketio_manager = SocketManager(app)

# socketio_manager = SocketManager(app, socketio_path="/socket.io")

# connect to the redis queue as an external process
# external_sio = socketio.RedisManager('redis://', write_only=True)

# emit an event
# external_sio.emit('my event', data={'foo': 'bar'}, room='my room')