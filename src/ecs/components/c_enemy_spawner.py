

import pygame


class CEnemySpawner:

        def __init__(self, events_data: dict) -> None:
            self.current_time: float = 0
            self.event_data: list[CEnemySpawnerData] = [] 
            for event in events_data:
                self.event_data.append(CEnemySpawnerData(event))

class CEnemySpawnerData:

        def __init__(self, event_data: dict) -> None:
            self.time = event_data.get('time')
            self.enemy_type = event_data.get('enemy_type')
            self.pos = pygame.Vector2(
                event_data.get('position').get('x'),
                event_data.get('position').get('y')
            )
            self.is_spawned = False