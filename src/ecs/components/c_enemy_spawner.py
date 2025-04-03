

import pygame


class CEnemySpawner:

        def __init__(self, time: float, pos_init: pygame.Vector2, is_spawned = False) -> None:
            self.time = time
            self.pos_init = pos_init
            self.is_spawned = is_spawned