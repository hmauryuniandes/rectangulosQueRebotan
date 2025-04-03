
import random
import esper
import pygame

from src.create.prefab_creator import create_enemy_rect
from src.ecs.components.c_enemy_spawner import CEnemySpawner, CEnemySpawnerData
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity


def system_enemy_spawner(ecs_world: esper.World, enemies_data: dict, delta_time: float) -> None:
   
    components = ecs_world.get_component(CEnemySpawner)
    c_s: CEnemySpawner

    for _, (c_s) in components:
        c_s.current_time += delta_time
        event: CEnemySpawnerData
        for event in c_s.event_data:
            if event.is_spawned == False and event.time <= c_s.current_time:
                event.is_spawned = True
                enemy_type = enemies_data[event.enemy_type]

                size = pygame.Vector2(enemy_type.get('size').get('x'), enemy_type.get('size').get('y'))
                color = pygame.Color(enemy_type.get('color').get('r'), enemy_type.get('color').get('g'), enemy_type.get('color').get('b'))

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

                create_enemy_rect(ecs_world, size, event.pos, vel, color)
   

        

        