
import pygame

from src.engine.service_locator import ServiceLocator


class CSurface:

    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.angle = 0
        self.area = self.surf.get_rect()
        self.original_surf = self.surf.copy()

    @classmethod
    def from_surface(cls, surf: pygame.Surface) -> 'CSurface':
        c_surf = cls((0, 0), (0, 0, 0))
        c_surf.surf = surf
        c_surf.area = surf.get_rect()
        c_surf.original_surf = surf.copy()
        return c_surf
    
    @classmethod
    def from_text(cls, text: str, color: pygame.Color) -> 'CSurface':
        c_surf = cls((0, 0), (0, 0, 0))
        c_surf.surf = ServiceLocator.fonts_service.get('assets/fnt/PressStart2P.ttf').render(text, True, color)
        c_surf.area = c_surf.surf.get_rect()
        c_surf.original_surf = c_surf.surf.copy()
        return c_surf
    
    def get_area_relative(self, area: pygame.Rect, pos_topleft: pygame.Vector2):
        new_rect = area.copy()
        new_rect.topleft = pos_topleft
        return new_rect