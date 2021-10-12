"""All Events"""

from src.utils.ws.adapter import EventWS
from src.utils.ws.channel import Channel
from src.utils.ws.message import Message
from src.utils.ws.server import Server

from . import Player, TicTacToe, PlayStatus


class Game:
    def __init__(self, player1: object, player2: object):
        self.player1 = Player(player1.uuid, player1.username)
        self.player2 = Player(player2.uuid, player2.username)
        self.tictactoe = TicTacToe(self.player1, self.player2)

    def get_player(self, uuid: str) -> Player:
        return self.player1 if self.player1.id == uuid else self.player2

    def get_other_player(self, uuid: str) -> Player:
        return self.player2 if self.player1.id == uuid else self.player1


class Play(EventWS):
    def __init__(self):
        self._event_title = "PLAY"

    def event(self, origin: str, channel: Channel,  message: dict, server: Server):
        username = message.get("username")
        message = Message(origin, origin)
        if username:
            # Creating Channel for User
            consumer = channel.get_consumer(origin)
            consumer.username = username
            consumer.uuid = origin
            server.channel(origin, consumer, origin)
            message.message = "done correctly"
            message.channel = origin
            channel.broadcast(origin, message)
        else:
            message.message = "error: username is required"
            channel.unicast("SERVER", [origin], message)



class Join(EventWS):
    def __init__(self):
        self._event_title = "JOIN"

    def event(self, origin: str, channel: Channel,  message: dict, server: Server):
        message_to_send = Message(origin, origin)
        if "game_id" not in message:
            message_to_send.message = "Error: attribute game_id is required"
            channel.unicast(origin, [origin], message_to_send)
        elif "username" not in message:
            message_to_send.message = "Error: username is required"
            channel.unicast(origin, [origin], message_to_send)
        else:
            id_channel = message.get("game_id")
            username = message.get("username")
            n_channel = server.get_channel(id_channel)
            if n_channel:
                if len(list(n_channel.consumers.values())) == 1:
                    # Player 1
                    other_consumer = list(n_channel.consumers.values())[0]
                    # Player 2
                    consumer = channel.get_consumer(origin)
                    consumer.username = username
                    consumer.uuid = origin
                    n_channel.add_consumer(consumer, origin)

                    # Add New Attribute to Channel, The Game
                    n_channel.instance = Game(other_consumer, consumer)

                    message_to_send.message = f"{username}: 2 users connected"
                    message_to_send.channel = id_channel
                    n_channel.broadcast(origin, message_to_send)
                else:
                    message_to_send.message = "Error: 2 user has already connected"
                    channel.unicast(origin, [origin], message_to_send)
            else:
                message_to_send.message = "Error: channel not found"
                channel.unicast(origin, [origin], message_to_send)


class Move(EventWS):
    def __init__(self):
        self._event_title = "MOVE"

    def event(self, origin: str, channel: Channel, message: dict, server: Server):
        requireds = ["move", "channel"]
        validation = True
        message_to_send = Message(origin, "SERVER")
        for required in requireds:
            if required not in message:
                validation = False
                message_to_send.message = f"Error: {required} is required"
                channel.unicast(origin, [origin], message_to_send)
        if validation:
            channel = message["channel"]
            game_channel = server.get_channel(channel)
            if game_channel:
                if game_channel.get_consumer(origin):
                    message_to_send.channel = game_channel.route
                    move = message["move"]
                    if int(move) > 0 and int(move) < 10:
                        status_game, player = game_channel.instance.tictactoe.play(move, game_channel.instance.get_player(origin))
                        message_to_send = Message(origin, game_channel.instance.get_other_player(origin).id)
                        message_to_send.channel = game_channel.route
                        message_to_send.message = move
                        game_channel.broadcast(origin, message_to_send)
                        if status_game in [PlayStatus.WIN, PlayStatus.DRAW]:
                            if status_game == PlayStatus.WIN:
                                message_to_send.message = f"win: {player.id}"
                            else:
                                message_to_send.message = "draw"
                            game_channel.broadcast(origin, message_to_send)
                            server.remove_channel(game_channel.route)
                    else:
                        message_to_send.message = "Error: move not valid"
                        channel.unicast(origin, [origin], message_to_send)
                else:
                    message_to_send.message = "Error: user is not in channel"
                    channel.unicast(origin, [origin], message_to_send)
            else:
                message_to_send.message = "Error: channel not found"
                channel.unicast(origin, [origin], message_to_send)


events = [
    Play,
    Join,
    Move,
]
