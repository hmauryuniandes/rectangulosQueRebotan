
import esper

from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.scenes.scene import Scene


def system_win(scene : Scene, world: esper.World):
    components = world.get_components(CTagEnemy)

    if len(components) == 0:
        scene.switch_scene("WIN_SCENE")
    