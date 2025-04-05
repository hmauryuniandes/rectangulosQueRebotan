
import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_bullet_limit(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagBullet) 

    c_t: CTransform
    c_s: CSurface
    c_t_p: CTagBullet

    for entity, (c_t, c_s, c_t_p) in components:
        cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)

        if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width:
            world.delete_entity(entity)

        if cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            world.delete_entity(entity)