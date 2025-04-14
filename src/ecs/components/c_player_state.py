from enum import Enum


class CPlayerState:
    def __init__(self):
        self.state = PlayerState.IDLE

class PlayerState(Enum):
    MOVE = 0
    IDLE = 1