

import esper
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_player_input import system_player_input
from src.ecs.systems.s_rendering import system_rendering


class Scene:
    def __init__(self, game_engine: 'src.engine.game_engine.GameEngine') -> None:
        self.ecs_world = esper.World()
        self._game_engine = game_engine
        self._screen_rect = game_engine.screen.get_rect()
        self.is_paused = False

    def do_process_event(self, event):
        system_player_input(self.ecs_world, event, self.do_action)

    def simulate(self, delta_time):
        self.do_update(delta_time)
        self.ecs_world._clear_dead_entities()

    def clean(self):
        self.ecs_world.clear_database()
        self.do_clean()

    def switch_scene(self, new_scene_name: str):
        self._game_engine.switch_scene(new_scene_name)

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen, self.is_paused)    

    def do_clean(self):
        pass
    
    def do_create(self):
        pass

    def do_update(self, delta_time: float):
        pass

    def do_action(self, action: CInputCommand):
        pass
