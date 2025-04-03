import json

def load_config():
    with open('assets/cfg/window.json', 'r') as file:
        window = json.load(file)

    with open('assets/cfg/enemies.json', 'r') as file:
        enemies = json.load(file)

    with open('assets/cfg/level_01.json', 'r') as file:
        level_01 = json.load(file)

    return (window, enemies, level_01)

