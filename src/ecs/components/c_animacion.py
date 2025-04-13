
import pygame


class CAnimation:

    def __init__(self, animation: dict) -> None:
        self.number_frames = animation.get('number_frames')
        self.animation_list: list[AnimationData] = []
        
        for anim in animation.get('list'):
            anim_data = AnimationData(
                name=anim.get('name'),
                start=anim.get('start'),
                end=anim.get('end'),
                framerate=anim.get('framerate')
            )
            self.animation_list.append(anim_data)
        
        self.current_animation = 0
        self.current_animation_time = 0
        self.current_frame = self.animation_list[self.current_animation].start

class AnimationData:
    def __init__(self, name: str, start: int, end: int, framerate: float) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0 / framerate