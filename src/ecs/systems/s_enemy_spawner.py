
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
                enemy_data = enemies_data[event.enemy_type]
                create_enemy_rect(ecs_world, enemy_data, event.pos)
   

        

        