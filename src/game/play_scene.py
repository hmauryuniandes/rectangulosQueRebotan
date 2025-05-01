

import json

import pygame
from src.create.prefab_creator import create_bomb, create_bullet, create_enemy_spawner, create_input_player, create_player_rect, create_text, create_text_bomb, create_text_pause
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_bomb_text import system_bomb_text
from src.ecs.systems.s_bullet_limit import system_bullet_limit
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_explosion_state import system_explosion_state
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_limit import system_player_limit
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_tele_bomb import system_tele_bomb
from src.ecs.systems.s_win import system_win
from src.engine.scenes.scene import Scene


class PlayScene(Scene):
    def __init__(self, path:str, engine: 'src.engine.game_engine.GameEngine'):
        super().__init__(engine)
        self.bomb_charge = 100
        with open(path, 'r') as file:
            self.level = json.load(file)

    def do_create(self):
        self._player_entity = create_player_rect(self.ecs_world, self._game_engine.player, self.level.get('player_spawn'))
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        create_enemy_spawner(self.ecs_world, self.level.get('enemy_spawn_events'))
        create_input_player(self.ecs_world)
        create_text(self.ecs_world, self._game_engine.interface.get("font"), self._game_engine.interface.get("title"), pygame.Vector2(20, 20))
        create_text(self.ecs_world, self._game_engine.interface.get("font"), self._game_engine.interface.get("help"), pygame.Vector2(20, 40))
        create_text_pause(self.ecs_world, self._game_engine.interface.get("font"), self._game_engine.interface.get("pause"), self._game_engine.screen)
        create_text_bomb(self.ecs_world, self._game_engine.interface.get("font"), self._game_engine.interface.get("bomb_text"), self._game_engine.screen)

    def do_update(self, delta_time: float):
        if not self._game_engine.is_paused:
            system_enemy_spawner(self.ecs_world, self._game_engine.enemies, delta_time)
            system_movement(self.ecs_world, delta_time)
            system_player_state(self.ecs_world)
            system_hunter_state(self.ecs_world, self._player_entity, self._game_engine.enemies.get("Hunter"))
            self.bomb_charge = system_tele_bomb(self.ecs_world, self._game_engine.screen, self._game_engine.bomb, self.bomb_charge, delta_time)
            system_bomb_text(self.ecs_world, self._game_engine.interface.get("font"), self._game_engine.interface.get("bomb_text"), self.bomb_charge)
            system_screen_bounce(self.ecs_world, self._game_engine.screen)
            system_bullet_limit(self.ecs_world, self._game_engine.screen)
            system_player_limit(self.ecs_world, self._game_engine.screen)
            system_collision_player_enemy(self, self.ecs_world, self._player_entity, self.level, self._game_engine.explosion)
            system_collision_bullet_enemy(self.ecs_world, self._game_engine.explosion)
            system_animation(self.ecs_world, delta_time)
            system_explosion_state(self.ecs_world)
            system_win(self, self.ecs_world)

            

    def do_action(self, c_input: CInputCommand):
        if not self._game_engine.is_paused:
            if c_input.name == "PLAYER_LEFT":
                if c_input.command_phase == CommandPhase.START:
                    self._player_c_v.vel.x -= self._game_engine.player.get('input_velocity')
                elif c_input.command_phase == CommandPhase.END:
                    self._player_c_v.vel.x += self._game_engine.player.get('input_velocity')
            elif c_input.name == "PLAYER_RIGHT":
                if c_input.command_phase == CommandPhase.START:
                    self._player_c_v.vel.x += self._game_engine.player.get('input_velocity')
                elif c_input.command_phase == CommandPhase.END:
                    self._player_c_v.vel.x -= self._game_engine.player.get('input_velocity')
            elif c_input.name == "PLAYER_UP":
                if c_input.command_phase == CommandPhase.START:
                    self._player_c_v.vel.y -= self._game_engine.player.get('input_velocity')
                elif c_input.command_phase == CommandPhase.END:
                    self._player_c_v.vel.y += self._game_engine.player.get('input_velocity')
            elif c_input.name == "PLAYER_DOWN":
                if c_input.command_phase == CommandPhase.START:
                    self._player_c_v.vel.y += self._game_engine.player.get('input_velocity')
                elif c_input.command_phase == CommandPhase.END:
                    self._player_c_v.vel.y -= self._game_engine.player.get('input_velocity')
            elif c_input.name == "PLAYER_FIRE":
                if c_input.command_phase == CommandPhase.START:
                    create_bullet(
                        self.ecs_world,
                        self._player_entity,
                        self._game_engine.bullet,
                        c_input.event_pos,
                        self.level.get("player_spawn").get("max_bullets")
                    )
            elif c_input.name == "PLAYER_BOMB":
                if c_input.command_phase == CommandPhase.START:
                    self.bomb_charge = create_bomb(
                        self.ecs_world,
                        self._player_entity,
                        self._game_engine.bomb,
                        c_input.event_pos,
                        self.bomb_charge
                    )

        if c_input.name == "PAUSE" and c_input.command_phase == CommandPhase.END:
            self._game_engine.is_paused = not self._game_engine.is_paused