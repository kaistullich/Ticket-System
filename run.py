from src import app
from src.config import socketio

if __name__ == '__main__':
    socketio.run(app)
