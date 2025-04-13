
import pygame


class CSurface:

    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()

    @classmethod
    def from_surface(cls, surf: pygame.Surface) -> 'CSurface':
        c_surf = cls((0, 0), (0, 0, 0))
        c_surf.surf = surf
        c_surf.area = surf.get_rect()

        return c_surf
    