from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on("connect")
def handleConnect():
    username = f"User{random.randint(1, 100)}"
    gender = random.choice(["girl", "boy"]) 
    avatar_url = f"https://avatar.iran.liara.run/public/{gender}?username={username}"

    users[request.sid] = {
        "username": username,
        "avatar": avatar_url
    }

    emit("user_joined", {"username": username, "avatar": avatar_url}, broadcast=True)
    emit("set_username", {"username": username})

@socketio.on("disconnect")
def handleDisconnect():
    user = users.pop(request.sid, None)
    if user:
        emit("user_left", {"username": user["username"]}, broadcast=True)

@socketio.on("send_message")
def handleMessage(data):
    user = users.get(request.sid)
    if user:
        emit("message_sent", {"username": user["username"], "avatar": user["avatar"], "message": data["message"]}, broadcast=True)

@socketio.on("update_username")
def handleUpdateUsername(data):
    old_username = users.get(request.sid)["username"]  # Corrected this line
    new_username = data["username"] 
    users[request.sid]["username"] = new_username
    emit("username_updated", {"old_username": old_username, "new_username": new_username}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
