import pyxel
import math
# je me suis servi de ce tuto pour faire ce raycasting : https://lodev.org/cgtutor/raycasting.html

WIDTH = 1280
HEIGHT = 720
CELL_SIZE = 64
FOV = math.pi / 3
NUM_RAYS = 320
RAY_WIDTH = WIDTH / NUM_RAYS
MAX_DEPTH = 400

pyxel.init(WIDTH, HEIGHT, title="Optimized 3D Maze", fps=60)

MAZE = [#jai pas reussi (encore) a faire un algo de generation de labyrinthe donc c'est un labyrinthe fixe
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,1,1,0,1,1,0,0,0,1,1,1,0,0,1,1,0,1,1,0,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,1,0,1,0,0,0,1,1,0,1,0,0,1,0,0,1,1,0,1,0,0,0,1,0,1,0,0,1,0,0,1,0,1],
    [1,0,1,0,1,1,0,1,0,1,1,1,0,1,0,0,1,1,0,1,1,0,1,0,0,1,1,1,0,1,0,1,1,0,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1,0,0,0,1,0,1,0,1,0,0,0,1,1,0,1,0,0,1,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,1,0,1,1,0,1,1,0,1,0,1,1,0,0,1,0,1,1,0,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,1,1,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,0,1,1,0,1,0,1,1,0,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,1],
    [1,0,1,0,1,1,0,1,0,1,1,1,1,0,1,1,1,1,0,0,1,1,0,1,1,0,1,1,0,1,0,1,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

player_x = CELL_SIZE * 1.5
player_y = CELL_SIZE * 1.5
player_angle = 0
player_speed = 2.5
rot_speed = 0.04

WALL_COLORS = [9, 10]

def precompute_ray_angles():
    return [(-FOV/2 + FOV * r / NUM_RAYS) for r in range(NUM_RAYS)]

RAY_ANGLES = precompute_ray_angles()

def update():
    global player_x, player_y, player_angle

    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
        player_angle -= rot_speed
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        player_angle += rot_speed

    dx = math.cos(player_angle) * player_speed
    dy = math.sin(player_angle) * player_speed

    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
        try_move(dx, dy)
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
        try_move(-dx, -dy)

def try_move(dx, dy):
    global player_x, player_y
    nx = player_x + dx
    ny = player_y + dy
    if not wall_at(nx, ny):
        player_x = nx
        player_y = ny

def wall_at(x, y):
    i = int(y // CELL_SIZE)
    j = int(x // CELL_SIZE)
    if i < 0 or i >= len(MAZE) or j < 0 or j >= len(MAZE[0]):
        return True
    return MAZE[i][j] == 1

def cast_ray(angle):
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    for depth in range(1, MAX_DEPTH):
        x = player_x + cos_a * depth
        y = player_y + sin_a * depth
        if wall_at(x, y):
            return depth
    return MAX_DEPTH

def draw():
    pyxel.cls(0)

    pyxel.rect(0, 0, WIDTH, HEIGHT//2, 3)
    pyxel.rect(0, HEIGHT//2, WIDTH, HEIGHT//2, 7)

    for i, rel_angle in enumerate(RAY_ANGLES):
        ray_angle = player_angle + rel_angle
        distance = cast_ray(ray_angle)
        distance *= math.cos(rel_angle) #sert a enlevr le fisheye effect
        
        wall_height = min(int(CELL_SIZE * 400 / (distance+0.001)), HEIGHT)

        shade_index = int(distance / 25) % len(WALL_COLORS)
        color = WALL_COLORS[shade_index]

        x = int(i * RAY_WIDTH)
        pyxel.rect(x, HEIGHT//2 - wall_height//2, int(RAY_WIDTH)+1, wall_height, color)

#minimap
    map_scale = 8
    for row_i, row in enumerate(MAZE):
        for col_j, cell in enumerate(row):
            color = 0 if cell == 0 else 8
            pyxel.rect(col_j*map_scale, row_i*map_scale, map_scale-1, map_scale-1, color)
    pyxel.circ(int(player_x / CELL_SIZE * map_scale), int(player_y / CELL_SIZE * map_scale), 2, 11)

pyxel.run(update, draw)
