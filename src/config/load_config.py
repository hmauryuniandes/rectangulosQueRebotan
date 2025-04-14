import json

def load_config():
    with open('assets/cfg/window.json', 'r') as file:
        window = json.load(file)

    with open('assets/cfg/enemies.json', 'r') as file:
        enemies = json.load(file)

    with open('assets/cfg/level_01.json', 'r') as file:
        level_01 = json.load(file)

    with open('assets/cfg/player.json', 'r') as file:
        player = json.load(file)

    with open('assets/cfg/bullet.json', 'r') as file:
        bullet = json.load(file)
    
    with open('assets/cfg/explosion.json', 'r') as file:
        explosion = json.load(file)


    return (window, enemies, level_01, player, bullet, explosion)

