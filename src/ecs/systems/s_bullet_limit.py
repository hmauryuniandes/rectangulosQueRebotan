
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
        bullet_rect = c_s.area.copy()
        bullet_rect.topleft = c_t.pos

        if not screen_rect.contains(bullet_rect):
            world.delete_entity(entity)