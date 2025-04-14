from enum import Enum


class CHunterState:
    def __init__(self):
        self.state = HunterState.IDLE

class HunterState(Enum):
    MOVE = 0
    IDLE = 1