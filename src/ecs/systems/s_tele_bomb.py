
import math
import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bomb import CTagBomb
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_tele_bomb(world: esper.World, screen: pygame.Surface, bomb_info: dict):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CVelocity, CTagBomb) 

    c_t: CTransform
    c_s: CSurface
    c_v: CVelocity
    c_t_p: CTagBomb

    for entity, (c_t, c_s, c_v, c_t_p) in components:
        enemy_id = get_closest_enemy(world, c_t.pos)
        if enemy_id is not None:
            enemy_t  = world.component_for_entity(enemy_id, CTransform)
            direction = (enemy_t.pos - c_t.pos).normalize()
            c_v.vel = direction * bomb_info.get("velocity") 
            new_angle = math.degrees(math.atan2(c_v.vel.y, c_v.vel.x))
            c_s.surf = pygame.transform.rotate(c_s.original_surf.copy(), new_angle * -1)

def get_closest_enemy(world: esper.World, bomb_pos: pygame.Vector2):
    enemies = world.get_components(CTransform, CTagEnemy)
    closest_enemy = None
    min_distance = float('inf')

    c_t: CTransform
    c_e: CTagEnemy
    
    for enemy, (c_t, c_e) in enemies:
        distance = math.hypot(c_t.pos.x - bomb_pos.x, c_t.pos.y - bomb_pos.y)
        
        if distance < min_distance:
            min_distance = distance
            closest_enemy = enemy
    
    return closest_enemy