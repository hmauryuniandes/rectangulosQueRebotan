

import esper
import pygame
import random 

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def create_cuad(ecs_world: esper.World,
                   size: pygame.Vector2,
                   pos: pygame.Vector2,
                   vel: pygame.Vector2,
                   col: pygame.Color):
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity, CSurface(size, col))
    ecs_world.add_component(cuad_entity, CTransform(pos))
    ecs_world.add_component(cuad_entity, CVelocity(vel))

def create_enemies(ecs_world: esper.World, enemies: dict, level: dict):

    for event in level.get('enemy_spawn_events'):
        enemy_entity = ecs_world.create_entity()

        enemy_type = enemies.get(event.get('enemy_type'))

        size = pygame.Vector2(enemy_type.get('size').get('x'), enemy_type.get('size').get('y'))
        color = pygame.Color(enemy_type.get('color').get('r'), enemy_type.get('color').get('g'), enemy_type.get('color').get('b'))
        pos = pygame.Vector2(event.get('position').get('x'), event.get('position').get('y'))
        time = float(event.get('time'))

        # Random velocity between min and max
        random_vel_x = random.uniform(float(enemy_type.get('velocity_min')), float(enemy_type.get('velocity_max')))
        random_vel_y = random.uniform(float(enemy_type.get('velocity_min')), float(enemy_type.get('velocity_max')))

        # The angle of direction in which each rectangle moves is random.
        invert_x = random.choice([True, False])
        if invert_x:
            random_vel_x *= -1

        invert_y = random.choice([True, False])
        if invert_y:
            random_vel_y *= -1

        vel = pygame.Vector2(random_vel_x,random_vel_y)

        ecs_world.add_component(enemy_entity, CSurface(size, color))
        ecs_world.add_component(enemy_entity, CVelocity(vel))
        ecs_world.add_component(enemy_entity, CEnemySpawner(time, pos))
        # ecs_world.add_component(enemy_entity, CTransform(pos))