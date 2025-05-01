import json

def load_config():
    with open('assets/cfg/window.json', 'r') as file:
        window = json.load(file)

    with open('assets/cfg/enemies.json', 'r') as file:
        enemies = json.load(file)

    with open('assets/cfg/player.json', 'r') as file:
        player = json.load(file)

    with open('assets/cfg/bullet.json', 'r') as file:
        bullet = json.load(file)
    
    with open('assets/cfg/explosion.json', 'r') as file:
        explosion = json.load(file)
    
    with open('assets/cfg/interface.json', 'r') as file:
        interface = json.load(file)

    with open('assets/cfg/bomb.json', 'r') as file:
        bomb = json.load(file)



    return (window, enemies, player, bullet, explosion, interface, bomb)

