


import esper
from src.ecs.components.c_animacion import CAnimation
from src.ecs.components.c_surface import CSurface


def system_animation(world: esper.World, delta_time: float) -> None:
    components = world.get_components(CSurface, CAnimation)
    c_s: CSurface
    c_a: CAnimation

    for _, (c_s, c_a) in components:
        # Reduce current time
        c_a.current_animation_time -= delta_time

        # Check if current time is less than 0
        if c_a.current_animation_time <= 0:
            # Reset current time
            c_a.current_animation_time = c_a.animation_list[c_a.current_animation].framerate
            # change frame
            c_a.current_frame += 1

            # Limit frame based on start and end
            if c_a.current_frame > c_a.animation_list[c_a.current_animation].end:
                c_a.current_frame = c_a.animation_list[c_a.current_animation].start

            # Recalculate sub area of the sprite sheet
            rect_surf = c_s.surf.get_rect()
            c_s.area.w = rect_surf.w / c_a.number_frames
            c_s.area.x = c_s.area.w * c_a.current_frame
