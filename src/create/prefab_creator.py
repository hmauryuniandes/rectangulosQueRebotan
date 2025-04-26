

import esper
import pygame
import random 

from src.ecs.components.c_animacion import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bomb import CTagBomb
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.ecs.components.tags.c_tag_pause import CTagPuase
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def create_square(ecs_world: esper.World,
                   size: pygame.Vector2,
                   pos: pygame.Vector2,
                   vel: pygame.Vector2,
                   col: pygame.Color):
    square_entity = ecs_world.create_entity()
    ecs_world.add_component(square_entity, CSurface(size, col))
    ecs_world.add_component(square_entity, CTransform(pos))
    ecs_world.add_component(square_entity, CVelocity(vel))
    return square_entity

def create_sprint(ecs_world: esper.World,
                   pos: pygame.Vector2,
                   vel: pygame.Vector2,
                   surf: pygame.Surface) -> int:
    sprite_entity = ecs_world.create_entity()
    ecs_world.add_component(sprite_entity, CTransform(pos))
    ecs_world.add_component(sprite_entity, CVelocity(vel))
    # surf = pygame.transform.rotate(surf, -180)
    ecs_world.add_component(sprite_entity, CSurface.from_surface(surf))


    return sprite_entity

def create_player_rect(ecs_world: esper.World, player: dict, player_spawn: dict) -> None:
    vel = pygame.Vector2(0, 0)
    player_surface = ServiceLocator.images_service.get(player.get('image'))
    size = player_surface.get_size()
    size = (size[0] / player.get('animations').get('number_frames'), size[1])
    pos = pygame.Vector2(
        player_spawn.get('position').get('x') - size[0] / 2,
        player_spawn.get('position').get('y') - size[1] / 2
    )
    player_entity = create_sprint(ecs_world, pos, vel, player_surface)
    ecs_world.add_component(player_entity, CTagPlayer())
    ecs_world.add_component(player_entity, CAnimation(player.get('animations')))
    ecs_world.add_component(player_entity, CPlayerState())
    return player_entity

def create_enemy_rect(ecs_world: esper.World, enemy_data: dict, pos: pygame.Vector2) -> None:
    enemy_surface = ServiceLocator.images_service.get(enemy_data.get('image'))
    # Random velocity between min and max
    random_vel_x = random.uniform(float(enemy_data.get('velocity_min')), float(enemy_data.get('velocity_max')))
    random_vel_y = random.uniform(float(enemy_data.get('velocity_min')), float(enemy_data.get('velocity_max')))

    # The angle of direction in which each rectangle moves is random.
    invert_x = random.choice([True, False])
    if invert_x:
        random_vel_x *= -1

    invert_y = random.choice([True, False])
    if invert_y:
        random_vel_y *= -1

    vel = pygame.Vector2(random_vel_x,random_vel_y)
    enemy_entity = create_sprint(ecs_world, pos, vel, enemy_surface)
    ecs_world.add_component(enemy_entity, CTagEnemy())
    ServiceLocator.sounds_service.play(enemy_data.get("sound"))

def create_hunter_rect(ecs_world: esper.World, hunter_data: dict, pos: pygame.Vector2) -> None:
    hunter_surface = ServiceLocator.images_service.get(hunter_data.get('image'))
    vel = pygame.Vector2(0, 0)
    enemy_entity = create_sprint(ecs_world, pos, vel, hunter_surface)
    ecs_world.add_component(enemy_entity, CTagEnemy())
    ecs_world.add_component(enemy_entity, CTagHunter())
    ecs_world.add_component(enemy_entity, CHunterState())
    ecs_world.add_component(enemy_entity, CAnimation(hunter_data.get('animations')))

def create_enemy_spawner(ecs_world: esper.World, level_data: dict):
    spawner_entity = ecs_world.create_entity()
    ecs_world.add_component(spawner_entity, CEnemySpawner(level_data))
  
def create_input_player(ecs_world: esper.World) -> None:
    input_left = ecs_world.create_entity()
    input_right = ecs_world.create_entity()
    input_up = ecs_world.create_entity()
    input_down = ecs_world.create_entity()
    input_left_click = ecs_world.create_entity()
    input_right_click = ecs_world.create_entity()
    input_pause = ecs_world.create_entity()
    
    ecs_world.add_component(input_left, CInputCommand("PLAYER_LEFT", [pygame.K_LEFT, pygame.K_a], []))
    ecs_world.add_component(input_right, CInputCommand("PLAYER_RIGHT", [pygame.K_RIGHT, pygame.K_d], []))
    ecs_world.add_component(input_up, CInputCommand("PLAYER_UP", [pygame.K_UP, pygame.K_w], []))
    ecs_world.add_component(input_down, CInputCommand("PLAYER_DOWN", [pygame.K_DOWN, pygame.K_s], []))
    ecs_world.add_component(input_left_click, CInputCommand("PLAYER_FIRE", [], [pygame.BUTTON_LEFT]))
    ecs_world.add_component(input_right_click, CInputCommand("PLAYER_BOMB", [], [pygame.BUTTON_RIGHT]))
    ecs_world.add_component(input_pause, CInputCommand("PAUSE", [pygame.K_p], []))

def create_bullet(ecs_world: esper.World,  player_entity: int, bullet: dict, event_pos: pygame.Vector2, max_bullets: int) -> None:
    
    if len(ecs_world.get_components(CTagBullet)) < max_bullets:
        pl_t: CTransform  = ecs_world.component_for_entity(player_entity, CTransform)
        pl_s: CSurface  = ecs_world.component_for_entity(player_entity, CSurface)

        pl_rect = pl_s.get_area_relative(pl_s.area, pl_t.pos)
        direction = (pygame.Vector2(event_pos) - pygame.Vector2(pl_rect.center)).normalize()
        vel = direction * bullet.get("velocity")
        bullet_surface = ServiceLocator.images_service.get(bullet.get('image'))
        bullet_size = bullet_surface.get_size()
        pos = pygame.Vector2(pl_rect.center[0] - (bullet_size[0] / 2), pl_rect.center[1] - (bullet_size[1] / 2))
        bullet_entity = create_sprint(ecs_world, pos, vel, bullet_surface)
        ServiceLocator.sounds_service.play(bullet.get("sound"))
        ecs_world.add_component(bullet_entity, CTagBullet())


def create_bomb(ecs_world: esper.World,  player_entity: int, bomb: dict, event_pos: pygame.Vector2, bomb_charge: int) -> None:
    
    if bomb_charge == 100:
        pl_t: CTransform  = ecs_world.component_for_entity(player_entity, CTransform)
        pl_s: CSurface  = ecs_world.component_for_entity(player_entity, CSurface)

        pl_rect = pl_s.get_area_relative(pl_s.area, pl_t.pos)
        direction = (pygame.Vector2(event_pos) - pygame.Vector2(pl_rect.center)).normalize()
        vel = direction * bomb.get("velocity")
        bullet_surface = ServiceLocator.images_service.get(bomb.get('image'))
        bullet_size = bullet_surface.get_size()
        pos = pygame.Vector2(pl_rect.center[0] - (bullet_size[0] / 2), pl_rect.center[1] - (bullet_size[1] / 2))
        bullet_entity = create_sprint(ecs_world, pos, vel, bullet_surface)
        ServiceLocator.sounds_service.play(bomb.get("sound"))
        ecs_world.add_component(bullet_entity, CTagBullet())
        ecs_world.add_component(bullet_entity, CTagBomb())

def create_explosion(ecs_world: esper.World, pos: pygame.Vector2, explosion: dict):
    surf = ServiceLocator.images_service.get(explosion.get("image"))
    vel = pygame.Vector2(0, 0)
    explosion_entity = create_sprint(ecs_world, pos, vel, surf)
    ecs_world.add_component(explosion_entity, CTagExplosion())
    ecs_world.add_component(explosion_entity, CAnimation(explosion.get("animations")))
    ServiceLocator.sounds_service.play(explosion.get("sound"))
    return explosion_entity

def create_text_pause(ecs_world: esper.World, text: str, screen: pygame.Surface) -> None:
    screen_rect = screen.get_rect()
    vel = pygame.Vector2(0, 0)
    surface = CSurface.from_text(text, (255, 255, 255))
    surface.area.width
    pos = pygame.Vector2(
        screen_rect.centerx - surface.area.width / 2,
        screen_rect.centery - surface.area.height / 2
    )

    entity = ecs_world.create_entity()
    ecs_world.add_component(entity, surface)
    ecs_world.add_component(entity, CTransform(pos))
    ecs_world.add_component(entity, CVelocity(vel))
    ecs_world.add_component(entity, CTagPuase())
    return entity

def create_text_title(ecs_world: esper.World, text: str, screen: pygame.Surface) -> None:
    screen_rect = screen.get_rect()
    surface = CSurface.from_text(text, (255, 255, 255))
    vel = pygame.Vector2(0, 0)
    surface.area.width
    pos = pygame.Vector2(
        screen_rect.centerx - surface.area.width / 2,
        0
    )
    
    entity = ecs_world.create_entity()
    ecs_world.add_component(entity, surface)
    ecs_world.add_component(entity, CTransform(pos))
    ecs_world.add_component(entity, CVelocity(vel))
    return entity