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

class App:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent
        song_path = base_dir / "song2.mp3"
        self.player = vlc.MediaPlayer(str(song_path))
        self.player.play()

        # pl init state
        self.posX = 22
        self.posY = 12
        self.dirX = -1
        self.dirY = 0
        self.planeX = 0
        self.planeY = 0.66

        # nextbot init
        self.botX = 5
        self.botY = 5

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Raycaster")
        pyxel.mouse(True)

        # store mousex
        self.last_mouse_x = pyxel.mouse_x

        pyxel.run(self.update, self.draw)

    def update(self):
        moveSpeed = 0.2
        botSpeed = 0.1
        sensitivity = 0.003  # mouse sensitivity

        # player movement 
        rotSpeed = 0.15 #sets player rotation speed
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z):
            if worldMap[int(self.posX + self.dirX * moveSpeed)][int(self.posY)] == 0:
                self.posX += self.dirX * moveSpeed
            if worldMap[int(self.posX)][int(self.posY + self.dirY * moveSpeed)] == 0:
                self.posY += self.dirY * moveSpeed

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            if worldMap[int(self.posX - self.dirX * moveSpeed)][int(self.posY)] == 0:
                self.posX -= self.dirX * moveSpeed
            if worldMap[int(self.posX)][int(self.posY - self.dirY * moveSpeed)] == 0:
                self.posY -= self.dirY * moveSpeed

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q):
            angle = rotSpeed
            oldDirX = self.dirX
            self.dirX = self.dirX * math.cos(angle) - self.dirY * math.sin(angle)
            self.dirY = oldDirX * math.sin(angle) + self.dirY * math.cos(angle)

            oldPlaneX = self.planeX
            self.planeX = self.planeX * math.cos(angle) - self.planeY * math.sin(angle)
            self.planeY = oldPlaneX * math.sin(angle) + self.planeY * math.cos(angle)

        # rotate right (RIGHT arrow or D key)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            angle = -rotSpeed
            oldDirX = self.dirX
            self.dirX = self.dirX * math.cos(angle) - self.dirY * math.sin(angle)
            self.dirY = oldDirX * math.sin(angle) + self.dirY * math.cos(angle)

            oldPlaneX = self.planeX
            self.planeX = self.planeX * math.cos(angle) - self.planeY * math.sin(angle)
            self.planeY = oldPlaneX * math.sin(angle) + self.planeY * math.cos(angle)

        # mouse deltax
        mouse_dx = pyxel.mouse_x - self.last_mouse_x
        angle = -mouse_dx * sensitivity

        if angle != 0:
            oldDirX = self.dirX
            self.dirX = self.dirX * math.cos(angle) - self.dirY * math.sin(angle)
            self.dirY = oldDirX * math.sin(angle) + self.dirY * math.cos(angle)

            oldPlaneX = self.planeX
            self.planeX = self.planeX * math.cos(angle) - self.planeY * math.sin(angle)
            self.planeY = oldPlaneX * math.sin(angle) + self.planeY * math.cos(angle)

        # mouse pos upd
        self.last_mouse_x = pyxel.mouse_x

        # nextbot simple follow with collision
        dx = self.posX - self.botX
        dy = self.posY - self.botY
        dist = math.hypot(dx, dy)
        if dist > 0.1:
            moveX = (dx / dist) * botSpeed
            moveY = (dy / dist) * botSpeed
            # collision check
            if worldMap[int(self.botX + moveX)][int(self.botY)] == 0:
                self.botX += moveX
            if worldMap[int(self.botX)][int(self.botY + moveY)] == 0:
                self.botY += moveY

    def draw(self):
        pyxel.cls(0)

        # draw world
        for x in range(SCREEN_WIDTH):
            cameraX = 2 * x / SCREEN_WIDTH - 1
            rayDirX = self.dirX + self.planeX * cameraX
            rayDirY = self.dirY + self.planeY * cameraX

            mapX = int(self.posX)
            mapY = int(self.posY)

            deltaDistX = abs(1 / rayDirX) if rayDirX != 0 else 1e30
            deltaDistY = abs(1 / rayDirY) if rayDirY != 0 else 1e30

            if rayDirX < 0:
                stepX = -1
                sideDistX = (self.posX - mapX) * deltaDistX
            else:
                stepX = 1
                sideDistX = (mapX + 1 - self.posX) * deltaDistX

            if rayDirY < 0:
                stepY = -1
                sideDistY = (self.posY - mapY) * deltaDistY
            else:
                stepY = 1
                sideDistY = (mapY + 1 - self.posY) * deltaDistY

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
        dx = self.botX - self.posX
        dy = self.botY - self.posY
        invDet = 1.0 / (self.planeX * self.dirY - self.dirX * self.planeY)
        transformX = invDet * (self.dirY * dx - self.dirX * dy)
        transformY = invDet * (-self.planeY * dx + self.planeX * dy)
        if transformY > 0:
            spriteScreenX = int((SCREEN_WIDTH / 2) * (1 + transformX / transformY))
            spriteHeight = int(SCREEN_HEIGHT / transformY)
            drawStartY = max(0, SCREEN_HEIGHT//2 - spriteHeight//2)
            drawEndY = min(SCREEN_HEIGHT-1, SCREEN_HEIGHT//2 + spriteHeight//2)
            pyxel.line(spriteScreenX, drawStartY, spriteScreenX, drawEndY, 10)

App()
