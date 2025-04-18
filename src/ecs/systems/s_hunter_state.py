import esper
import pygame

from src.ecs.components.c_animacion import CAnimation
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_hunter import CTagHunter


def system_hunter_state(world: esper.World, player_entity: int, hunter: dict):
    components = world.get_components(CVelocity, CTransform, CAnimation, CHunterState, CTagHunter)
    pl_t  = world.component_for_entity(player_entity, CTransform)

    for _, (c_v, c_t, c_a, c_pst, c_th) in components:
        if c_pst.state == HunterState.IDLE:
            _do_idle_state(c_v, c_t, c_a, c_pst, pl_t, hunter)
        elif c_pst.state == HunterState.MOVE:
            _do_move_state(c_v, c_t, c_a, c_pst, pl_t, hunter)

def _do_idle_state(c_v: CVelocity, c_t: CTransform, c_a: CAnimation, c_pst: CHunterState, player_t: CTransform, hunter: dict):
    _set_animation(c_a, 1)
    
    dist = player_t.pos.distance_to(c_t.pos)
    dist_initial_pos = c_t.pos.distance_to(c_t.initial_pos)

    if dist < hunter.get("distance_start_chase") or (dist > hunter.get("distance_start_return") and dist_initial_pos > 5):
        c_pst.state = HunterState.MOVE
    else: 
        c_v.vel = pygame.Vector2(0, 0)
        c_t.pos = c_t.initial_pos.copy()          
   

def _do_move_state(c_v: CVelocity, c_t: CTransform, c_a: CAnimation, c_pst: CHunterState, player_t: CTransform, hunter: dict):
    _set_animation(c_a, 0)
    
    dist = player_t.pos.distance_to(c_t.pos)
    dist_initial_pos = c_t.pos.distance_to(c_t.initial_pos)

    print(dist)
    print(dist_initial_pos)
    if dist >= hunter.get("distance_start_return") and dist_initial_pos <= 5:
        c_pst.state = HunterState.IDLE
    else: 
        if dist < hunter.get("distance_start_return"):
            direction = (player_t.pos - c_t.pos).normalize()
            c_v.vel = direction * hunter.get("velocity_chase")
        else:
            direction = (c_t.initial_pos - c_t.pos).normalize()
            c_v.vel = direction * hunter.get("velocity_return")

def _set_animation(c_a: CAnimation, num_animation: int):
    if c_a.current_animation == num_animation:
        return
    
    c_a.current_animation = num_animation
    c_a.current_animation_time = 0
    c_a.current_frame = c_a.animation_list[c_a.current_animation].start