

import pygame
from src.create.prefab_creator import create_input_quit_to_menu, create_text
from src.ecs.components.c_input_command import CInputCommand
from src.engine.scenes.scene import Scene


class GameOverScene(Scene):
    
    def __init__(self, engine: 'src.engine.game_engine.GameEngine'):
            super().__init__(engine)

    def do_create(self):
        create_text(self.ecs_world, self._game_engine.interface.get("font"), self._game_engine.interface.get("title"), pygame.Vector2(20, 20))
        create_text(self.ecs_world, self._game_engine.interface.get("font"), self._game_engine.interface.get("game_over"), pygame.Vector2(20, 90))
        create_input_quit_to_menu(self.ecs_world)

    def do_action(self, c_input: CInputCommand):
        if c_input.name == "QUIT_TO_MENU":
           self.switch_scene("MENU_SCENE")