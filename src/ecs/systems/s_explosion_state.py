import esper

from src.ecs.components.c_animacion import CAnimation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_explosion import CTagExplosion


def system_explosion_state(world: esper.World):
    components = world.get_components(CAnimation, CTagExplosion)

    for entity, (c_a, c_te) in components:
        if c_a.animation_list[c_a.current_animation].end == c_a.current_frame:
            world.delete_entity(entity)