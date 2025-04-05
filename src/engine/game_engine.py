
"""Modulo del motor del juego"""

import esper
import pygame

from src.config.load_config import load_config
from src.create.prefab_creator import create_bullet, create_enemy_spawner, create_input_player, create_player_rect
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_bullet_limit import system_bullet_limit
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_input import system_player_input
from src.ecs.systems.s_player_limit import system_player_limit
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce

class GameEngine:
    """La clase principal del motor de juego"""
    def __init__(self) -> None:
        (self.window, self.enemies, self.level_01, self.player, self.bullet) = load_config()

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
        self._player_entity = create_player_rect(self.ecs_world, self.player, self.level_01.get('player_spawn'))
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        create_enemy_spawner(self.ecs_world, self.level_01.get('enemy_spawn_events'))
        create_input_player(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_player_input(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_enemy_spawner(self.ecs_world, self.enemies, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
        system_player_limit(self.ecs_world, self.screen)
        system_bullet_limit(self.ecs_world, self.screen)
        system_collision_player_enemy(self.ecs_world, self._player_entity, self.level_01)
        system_collision_bullet_enemy(self.ecs_world)
        self.ecs_world._clear_dead_entities()

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
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand) -> None:
        if c_input.name == "PLAYER_LEFT":
            if c_input.command_phase == CommandPhase.START:
                self._player_c_v.vel.x -= self.player.get('input_velocity')
            elif c_input.command_phase == CommandPhase.END:
                self._player_c_v.vel.x += self.player.get('input_velocity')
        elif c_input.name == "PLAYER_RIGHT":
            if c_input.command_phase == CommandPhase.START:
                self._player_c_v.vel.x += self.player.get('input_velocity')
            elif c_input.command_phase == CommandPhase.END:
                self._player_c_v.vel.x -= self.player.get('input_velocity')
        elif c_input.name == "PLAYER_UP":
            if c_input.command_phase == CommandPhase.START:
                self._player_c_v.vel.y -= self.player.get('input_velocity')
            elif c_input.command_phase == CommandPhase.END:
                self._player_c_v.vel.y += self.player.get('input_velocity')
        elif c_input.name == "PLAYER_DOWN":
            if c_input.command_phase == CommandPhase.START:
                self._player_c_v.vel.y += self.player.get('input_velocity')
            elif c_input.command_phase == CommandPhase.END:
                self._player_c_v.vel.y -= self.player.get('input_velocity')
        elif c_input.name == "PLAYER_FIRE":
            if c_input.command_phase == CommandPhase.START:
                create_bullet(
                    self.ecs_world,
                    self._player_entity,
                    self.bullet,
                    c_input.event_pos,
                    self.level_01.get("player_spawn").get("max_bullets")
                )
            elif c_input.command_phase == CommandPhase.END:
                pass