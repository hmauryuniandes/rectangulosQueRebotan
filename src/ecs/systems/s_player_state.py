import esper

from src.ecs.components.c_animacion import CAnimation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_velocity import CVelocity


def system_player_state(world: esper.World):
    components = world.get_components(CVelocity, CAnimation, CPlayerState)

    for _, (c_v, c_a, c_pst) in components:
        if c_pst.state == PlayerState.IDLE:
            _do_idle_state(c_v, c_a, c_pst)
        elif c_pst.state == PlayerState.MOVE:
            _do_move_state(c_v, c_a, c_pst)

def _do_idle_state(c_v: CVelocity, c_a: CAnimation, c_pst: CPlayerState):
    _set_animation(c_a, 1)
    if c_v.vel.magnitude_squared() > 0:
        c_pst.state = PlayerState.MOVE

def _do_move_state(c_v: CVelocity, c_a: CAnimation, c_pst: CPlayerState):
    _set_animation(c_a, 0)
    if c_v.vel.magnitude_squared() <= 0:
        c_pst.state = PlayerState.IDLE

def _set_animation(c_a: CAnimation, num_animation: int):
    if c_a.current_animation == num_animation:
        return
    
    c_a.current_animation = num_animation
    c_a.current_animation_time = 0
    c_a.current_frame = c_a.animation_list[c_a.current_animation].start