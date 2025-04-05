from enum import Enum

import pygame

class CInputCommand:
    def __init__(self, name: str, key: int) -> None:
        self.name = name
        self.key = key
        self.command_phase = CommandPhase.NA
        self.event_pos: pygame.Vector2 = None
       
class CommandPhase(Enum):
    NA = 0
    START = 1
    END = 2
    