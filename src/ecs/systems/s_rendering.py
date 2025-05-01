
import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_pause import CTagPuase


def system_rendering(world: esper.World, screen: pygame.Surface, is_paused: bool) -> None:
    components = world.get_components(CTransform, CSurface) 

    c_t: CTransform
    c_s: CSurface

    for entity, (c_t, c_s) in components:
        if (is_paused and world.has_component(entity, CTagPuase)) \
            or not is_paused and not world.has_component(entity, CTagPuase):
            rotated_surface = pygame.transform.rotate(c_s.surf, c_t.rotation)
            screen.blit(rotated_surface, c_t.pos, area=c_s.area)