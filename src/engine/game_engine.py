
"""Modulo del motor del juego"""

import esper
import pygame

from src.config.load_config import load_config
from src.create.prefab_creator import create_enemy_spawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce

class GameEngine:
    """La clase principal del motor de juego"""
    def __init__(self) -> None:
        (self.window, self.enemies, self.level_01) = load_config()

        pygame.init()
        pygame.display.set_caption(self.window.get('title').encode("latin_1").decode("utf_8"))
        self.screen = pygame.display.set_mode((self.window.get('size').get('w'), self.window.get('size').get('h')), pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = float(self.window.get('framerate'))
        self.delta_time = 0

        self.ecs_world = esper.World()

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        create_enemy_spawner(self.ecs_world, self.level_01.get('enemy_spawn_events'))

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_enemy_spawner(self.ecs_world, self.enemies, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)

    def _draw(self):
        self.screen.fill(
            (
                self.window.get('bg_color').get('r'),
                self.window.get('bg_color').get('g'), 
                self.window.get('bg_color').get('b')
            )
        )

        system_rendering(self.ecs_world, self.screen)

        pygame.display.flip()

    def _clean(self):
        pygame.quit()
