
"""Modulo del motor del juego"""

import asyncio
import json
import esper
import pygame

from src.config.load_config import load_config
from src.create.prefab_creator import create_bomb, create_bullet
from src.ecs.components.c_input_command import CInputCommand, CommandPhase

from src.engine.scenes.scene import Scene
from src.game.game_over_scene import GameOverScene
from src.game.menu_scene import MenuScene
from src.game.play_scene import PlayScene
from src.game.win_scene import WinScene

class GameEngine:
    """La clase principal del motor de juego"""
    def __init__(self) -> None:
        (self.window, self.enemies, self.player, self.bullet, self.explosion, self.interface, self.bomb) = load_config()

        pygame.init()
        pygame.display.set_caption(self.window.get('title').encode("latin_1").decode("utf_8"))
        self.screen = pygame.display.set_mode((self.window.get('size').get('w'), self.window.get('size').get('h')), pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = float(self.window.get('framerate'))
        self.delta_time = 0
        self.is_paused = False

        with open('assets/cfg/level_01.json', 'r') as file:
            self.level_01 = json.load(file)

        self._scenes: dict[str, Scene] = {}
        self._scenes['MENU_SCENE'] = MenuScene(self)
        self._scenes['LEVEL_01'] = PlayScene('assets/cfg/level_01.json', self)
        self._scenes['WIN_SCENE'] = WinScene(self)
        self._scenes['GAME_OVER_SCENE'] = GameOverScene(self)
        self._current_scene: Scene = None
        self._scene_name_to_switch: Scene = None

    async def run(self, start_scene_name: str) -> None:
        self.is_running = True
        self._current_scene = self._scenes[start_scene_name]
        self._create()
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_scene_switch()
            await asyncio.sleep(0)
        self._do_clean()

    def switch_scene(self, new_scene_name: str) -> None:
        self._scene_name_to_switch = new_scene_name

    def _create(self):
        self._current_scene.do_create()

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_event(event)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self._current_scene.simulate(self.delta_time)

    def _draw(self):
        self.screen.fill(
            (
                self.window.get('bg_color').get('r'),
                self.window.get('bg_color').get('g'), 
                self.window.get('bg_color').get('b')
            )
        )
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()

    def _handle_scene_switch(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    def _do_clean(self):
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand) -> None:
        self._current_scene.do_action(c_input)