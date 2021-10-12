"""WS Server"""

from typing import Tuple
from json import loads
from uuid import uuid4
from flask_sock import Sock

from src.utils.ws.message import Message
from src.utils.ws.server import Server


def json_convert(data: str) -> Tuple[bool, dict]:
    try:
        return True, loads(data)
    except Exception as exc:
        print("exc - ", exc)
        return False, None


def socket(socket: Sock, emitter: Server):

    @socket.route("/tictactoe")
    def tictactoe(ws, **kwargs):
        """Load Tic Tac Toe Server"""
        me_id = str(uuid4())
        emitter.channel("", ws, me_id)
        # Send A Connect Message And ID
        n_message = Message(me_id, "SERVER")
        n_message.message = "Connected Correctly"
        ws.send(str(n_message))

        while ws.connected:
            is_valid, content = json_convert(ws.receive())
            if is_valid:
                emitter.emitter.emit(me_id, emitter.get_channel(""), content, emitter)
            else:
                n_message.message = "Error in Json sended"
                ws.send(str(n_message))

    return socket
