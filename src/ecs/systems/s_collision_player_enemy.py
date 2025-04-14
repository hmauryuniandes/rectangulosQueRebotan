

import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_collision_player_enemy(world: esper.World, player_entity: int, level: dict, explosion: dict):
    componenets = world.get_components(CSurface, CTransform, CTagEnemy)
    pl_t  = world.component_for_entity(player_entity, CTransform)
    pl_s  = world.component_for_entity(player_entity, CSurface)

    pl_rect = pl_s.get_area_relative(pl_s.area, pl_t.pos)

    c_s: CSurface
    c_t: CTransform
    for enemy_entity, (c_s, c_t, _) in componenets:
        ene_rect = pl_s.get_area_relative(c_s.area, c_t.pos)
        
        if ene_rect.colliderect(pl_rect):
            world.delete_entity(enemy_entity)
            create_explosion(world, c_t.pos, explosion)
            # reset player position
            pl_t.pos.x = level["player_spawn"]["position"]["x"] - pl_s.area.width / 2
            pl_t.pos.y = level["player_spawn"]["position"]["y"] - pl_s.area.height / 2