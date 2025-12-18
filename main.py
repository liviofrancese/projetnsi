import pyxel
import math

WIDTH = 960
HEIGHT = 540
pyxel.init(WIDTH, HEIGHT, title= "3D MAZE", fps=60)

MAZE = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,1,0,1,0,1],
    [1,0,1,0,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,1,1,0,1],
    [1,0,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1],
]

CELL_SIZE = 64
FOV = math.pi / 3
NUM_RAYS = WIDTH
MAX_DEPTH = 800

player_x = CELL_SIZE *1.5
player_y = CELL_SIZE *1.5
player_angle = 0
player_speed = 2.5
rot_speed=0.04

def update():
    global player_x, player_y, player_angle

    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q)
        player_angle -= rot_speed
        
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_A)
        player_angle += rot_speed
        
    dx =
    dy =