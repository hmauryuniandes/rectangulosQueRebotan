from typing import Callable
import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand, CommandPhase


def system_player_input(
    world: esper.World,
    event: pygame.event.Event,
    do_action: Callable[[CInputCommand], None]
) -> None:
    components = world.get_component(CInputCommand)
    for _, c_input in components:
        if event.type == pygame.KEYDOWN and event.key == c_input.key:
            c_input.command_phase = CommandPhase.START
            do_action(c_input)
        elif event.type == pygame.KEYUP and event.key == c_input.key:
            c_input.command_phase = CommandPhase.END
            do_action(c_input)
