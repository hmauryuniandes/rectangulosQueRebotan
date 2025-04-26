

import pygame


class FontsService:
    def __init__(self):
        self._fonts = {}

    def get(self, path: str) -> pygame.Font:
        if (path not in self._fonts):
            self._fonts[path] =  pygame.font.Font(path)
        return self._fonts[path]