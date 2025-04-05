

import esper
import pygame
import random 

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


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

def create_player_rect(ecs_world: esper.World, player: dict, player_spawn: dict) -> None:
    size = pygame.Vector2(player.get('size').get('x'), player.get('size').get('y'))
    color = pygame.Color(player.get('color').get('r'), player.get('color').get('g'), player.get('color').get('b'))
    pos = pygame.Vector2(
        player_spawn.get('position').get('x') - player.get('size').get('x') / 2,
        player_spawn.get('position').get('y') - player.get('size').get('y') / 2
    )
    vel = pygame.Vector2(0, 0)
    player_entity = create_square(ecs_world, size, pos, vel, color)
    ecs_world.add_component(player_entity, CTagPlayer())
    return player_entity

def create_enemy_rect(ecs_world: esper.World, enemy_data: dict, pos: pygame.Vector2) -> None:
    size = pygame.Vector2(enemy_data.get('size').get('x'), enemy_data.get('size').get('y'))
    color = pygame.Color(enemy_data.get('color').get('r'), enemy_data.get('color').get('g'), enemy_data.get('color').get('b'))

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
    enemy_entity = create_square(ecs_world, size, pos, vel, color)
    ecs_world.add_component(enemy_entity, CTagEnemy())

def create_enemy_spawner(ecs_world: esper.World, level_data: dict):
    spawner_entity = ecs_world.create_entity()
    ecs_world.add_component(spawner_entity, CEnemySpawner(level_data))
  
def create_input_player(ecs_world: esper.World) -> None:
    input_left = ecs_world.create_entity()
    input_right = ecs_world.create_entity()
    input_up = ecs_world.create_entity()
    input_down = ecs_world.create_entity()

    input_a = ecs_world.create_entity()
    input_d = ecs_world.create_entity()
    input_w = ecs_world.create_entity()
    input_s = ecs_world.create_entity()
    
    input_left_click = ecs_world.create_entity()
    
    ecs_world.add_component(input_left, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    ecs_world.add_component(input_right, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    ecs_world.add_component(input_up, CInputCommand("PLAYER_UP", pygame.K_UP))
    ecs_world.add_component(input_down, CInputCommand("PLAYER_DOWN", pygame.K_DOWN))

    ecs_world.add_component(input_a, CInputCommand("PLAYER_LEFT", pygame.K_a))
    ecs_world.add_component(input_d, CInputCommand("PLAYER_RIGHT", pygame.K_d))
    ecs_world.add_component(input_w, CInputCommand("PLAYER_UP", pygame.K_w))
    ecs_world.add_component(input_s, CInputCommand("PLAYER_DOWN", pygame.K_s))

    ecs_world.add_component(input_left_click, CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT))

def create_bullet(ecs_world: esper.World,  player_entity: int, bullet: dict, event_pos: pygame.Vector2, max_bullets: int) -> None:
    
    if len(ecs_world.get_components(CTagBullet)) < max_bullets:
        pl_t: CTransform  = ecs_world.component_for_entity(player_entity, CTransform)
        pl_s: CSurface  = ecs_world.component_for_entity(player_entity, CSurface)

        pl_rect = pl_s.surf.get_rect(topleft = pl_t.pos)

        size = pygame.Vector2(bullet.get('size').get('x'), bullet.get('size').get('y'))
        color = pygame.Color(bullet.get('color').get('r'), bullet.get('color').get('g'), bullet.get('color').get('b'))
        pos = pygame.Vector2(pl_rect.center[0], pl_rect.center[1])
        direction = (pygame.Vector2(event_pos) - pygame.Vector2(pl_rect.center)).normalize()
        vel = pygame.Vector2(direction.x * bullet.get("velocity"), direction.y * bullet.get("velocity")) 

        bullet_entity = create_square(ecs_world, size, pos, vel, color)
        ecs_world.add_component(bullet_entity, CTagBullet())

    