
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bomb_text import CTagBombText


def system_bomb_text(world: esper.World, font: str, text: dict, bomb_charge: float):
    components = world.get_components(CSurface, CTagBombText) 

    c_s: CSurface
    c_b_t: CTagBombText

    for entity, (c_s, c_b_t) in components:
        new_surface = CSurface.from_text(font, text.get("text") + " " + str(int(bomb_charge)) + "%", text.get("color"), text.get("size"))
        c_s.surf = new_surface.surf
        c_s.area = c_s.surf.get_rect()