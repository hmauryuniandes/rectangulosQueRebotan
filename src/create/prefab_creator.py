

import esper
import pygame
import random 

from src.ecs.components.c_enemy_spawner import CEnemySpawner, CEnemySpawnerData
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def create_square(ecs_world: esper.World,
                   size: pygame.Vector2,
                   pos: pygame.Vector2,
                   vel: pygame.Vector2,
                   col: pygame.Color):
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity, CSurface(size, col))
    ecs_world.add_component(cuad_entity, CTransform(pos))
    ecs_world.add_component(cuad_entity, CVelocity(vel))

def create_player_rect(ecs_world: esper.World, player: dict, player_spawn: dict) -> None:
    size = pygame.Vector2(player.get('size').get('x'), player.get('size').get('y'))
    color = pygame.Color(player.get('color').get('r'), player.get('color').get('g'), player.get('color').get('b'))
    pos = pygame.Vector2(
        player_spawn.get('position').get('x') - player.get('size').get('x') / 2,
        player_spawn.get('position').get('y') - player.get('size').get('y') / 2
    )
    vel = pygame.Vector2(0, 0)
    create_square(ecs_world, size, pos, vel, color)

def create_enemy_rect(ecs_world: esper.World, enemy_data: dict, pos: pygame.Vector2) -> None:
    size = pygame.Vector2(enemy_data.get('size').get('x'), enemy_data.get('size').get('y'))
    color = pygame.Color(enemy_data.get('color').get('r'), enemy_data.get('color').get('g'), enemy_data.get('color').get('b'))

    # Random velocity between min and max
    random_vel_x = random.uniform(float(enemy_data.get('velocity_min')), float(enemy_data.get('velocity_max')))
    random_vel_y = random.uniform(float(enemy_data.get('velocity_min')), float(enemy_data.get('velocity_max')))

    # The angle of direction in which each rectangle moves is random.
    invert_x = random.choice([True, False])
    if invert_x:
        random_vel_x *= -1

    invert_y = random.choice([True, False])
    if invert_y:
        random_vel_y *= -1

    vel = pygame.Vector2(random_vel_x,random_vel_y)
    create_square(ecs_world, size, pos, vel, color)

def create_enemy_spawner(ecs_world: esper.World, level_data: dict):
    spawner_entity = ecs_world.create_entity()
    ecs_world.add_component(spawner_entity, CEnemySpawner(level_data))
  