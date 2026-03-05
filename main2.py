import pyxel
import math
import vlc
from pathlib import Path

SCREEN_WIDTH = 2560
SCREEN_HEIGHT = 1440

MAP_WIDTH = 24
MAP_HEIGHT = 24

worldMap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
    [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
    [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],    
    [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

base_dir = Path(__file__).resolve().parent
song_path = base_dir / "song2.mp3"
player = vlc.MediaPlayer(str(song_path))
player.play()

# pl init state
posX = 22
posY = 12
dirX = -1
dirY = 0
planeX = 0
planeY = 0.66

# nextbot init
botX = 5
botY = 5

pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Raycaster")
pyxel.mouse(True)

# store mousex
last_mouse_x = pyxel.mouse_x

def update():
    global posX,posY,dirX,dirY,planeX,planeY,botX,botY,last_mouse_x

    moveSpeed = 0.2
    botSpeed = 0.1
    sensitivity = 0.003  # mouse sensitivity

    # player movement 
    rotSpeed = 0.15 #sets player rotation speed
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z):
        if worldMap[int(posX + dirX * moveSpeed)][int(posY)] == 0:
            posX += dirX * moveSpeed
        if worldMap[int(posX)][int(posY + dirY * moveSpeed)] == 0:
            posY += dirY * moveSpeed

    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
        if worldMap[int(posX - dirX * moveSpeed)][int(posY)] == 0:
            posX -= dirX * moveSpeed
        if worldMap[int(posX)][int(posY - dirY * moveSpeed)] == 0:
            posY -= dirY * moveSpeed

    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q):
        angle = rotSpeed
        oldDirX = dirX
        dirX = dirX * math.cos(angle) - dirY * math.sin(angle)
        dirY = oldDirX * math.sin(angle) + dirY * math.cos(angle)

        oldPlaneX = planeX
        planeX = planeX * math.cos(angle) - planeY * math.sin(angle)
        planeY = oldPlaneX * math.sin(angle) + planeY * math.cos(angle)

    # rotate right (RIGHT arrow or D key)
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        angle = -rotSpeed
        oldDirX = dirX
        dirX = dirX * math.cos(angle) - dirY * math.sin(angle)
        dirY = oldDirX * math.sin(angle) + dirY * math.cos(angle)

        oldPlaneX = planeX
        planeX = planeX * math.cos(angle) - planeY * math.sin(angle)
        planeY = oldPlaneX * math.sin(angle) + planeY * math.cos(angle)

    # mouse deltax
    mouse_dx = pyxel.mouse_x - last_mouse_x
    angle = -mouse_dx * sensitivity

    if angle != 0:
        oldDirX = dirX
        dirX = dirX * math.cos(angle) - dirY * math.sin(angle)
        dirY = oldDirX * math.sin(angle) + dirY * math.cos(angle)

        oldPlaneX = planeX
        planeX = planeX * math.cos(angle) - planeY * math.sin(angle)
        planeY = oldPlaneX * math.sin(angle) + planeY * math.cos(angle)

    # mouse pos upd
    last_mouse_x = pyxel.mouse_x

    # nextbot simple follow with collision
    dx = posX - botX
    dy = posY - botY
    dist = math.hypot(dx, dy)
    if dist > 0.1:
        moveX = (dx / dist) * botSpeed
        moveY = (dy / dist) * botSpeed
        # collision check
        if worldMap[int(botX + moveX)][int(botY)] == 0:
            botX += moveX
        if worldMap[int(botX)][int(botY + moveY)] == 0:
            botY += moveY

def draw():
    pyxel.cls(0)

    # draw world
    for x in range(SCREEN_WIDTH):
        cameraX = 2 * x / SCREEN_WIDTH - 1
        rayDirX = dirX + planeX * cameraX
        rayDirY = dirY + planeY * cameraX

        mapX = int(posX)
        mapY = int(posY)

        deltaDistX = abs(1 / rayDirX) if rayDirX != 0 else 1e30
        deltaDistY = abs(1 / rayDirY) if rayDirY != 0 else 1e30

        if rayDirX < 0:
            stepX = -1
            sideDistX = (posX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1 - posX) * deltaDistX

        if rayDirY < 0:
            stepY = -1
            sideDistY = (posY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1 - posY) * deltaDistY

        hit = 0
        side = 0

        while hit == 0:
            if sideDistX < sideDistY:
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1

            if worldMap[mapX][mapY] > 0:
                hit = 1

        if side == 0:
            perpWallDist = sideDistX - deltaDistX
        else:
            perpWallDist = sideDistY - deltaDistY

        lineHeight = int(SCREEN_HEIGHT / perpWallDist)
        drawStart = max(0, -lineHeight // 2 + SCREEN_HEIGHT // 2)
        drawEnd = min(SCREEN_HEIGHT - 1, lineHeight // 2 + SCREEN_HEIGHT // 2)

        color = worldMap[mapX][mapY] % 16
        if side == 1:
            color = (color + 8) % 16

        pyxel.line(x, drawStart, x, drawEnd, color)

    # draw nextbot once per frame
    dx = botX - posX
    dy = botY - posY
    invDet = 1.0 / (planeX * dirY - dirX * planeY)
    transformX = invDet * (dirY * dx - dirX * dy)
    transformY = invDet * (-planeY * dx + planeX * dy)
    if transformY > 0:
        spriteScreenX = int((SCREEN_WIDTH / 2) * (1 + transformX / transformY))
        spriteHeight = int(SCREEN_HEIGHT / transformY)
        drawStartY = max(0, SCREEN_HEIGHT//2 - spriteHeight//2)
        drawEndY = min(SCREEN_HEIGHT-1, SCREEN_HEIGHT//2 + spriteHeight//2)
        pyxel.line(spriteScreenX, drawStartY, spriteScreenX, drawEndY, 10)

pyxel.run(update, draw)