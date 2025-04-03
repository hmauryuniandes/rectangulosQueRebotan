
import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_enemy_spawner(ecs_world: esper.World, game_time: float) -> None:
    components = ecs_world.get_components(CSurface, CVelocity, CEnemySpawner) 
    
    c_s: CSurface
    c_v: CVelocity
    c_e: CEnemySpawner
    for entity, (c_s, c_v, c_e) in components:
        if c_e.is_spawned == False and c_e.time <= game_time:
            ecs_world.add_component(entity, CTransform(c_e.pos_init))
            c_e.is_spawned = True