import pyxel
import math

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

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
        self.posX = 22
        self.posY = 12
        self.dirX = -1
        self.dirY = 0
        self.planeX = 0
        self.planeY = 0.66

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Raycaster")
        pyxel.run(self.update, self.draw)

    def update(self):
        moveSpeed = 0.2
        rotSpeed = 0.05

        #go forward
        if pyxel.btn(pyxel.KEY_UP):
            if worldMap[int(self.posX + self.dirX * moveSpeed)][int(self.posY)] == 0:
                self.posX += self.dirX * moveSpeed
            if worldMap[int(self.posX)][int(self.posY + self.dirY * moveSpeed)] == 0:
                self.posY += self.dirY * moveSpeed

        #go backward
        if pyxel.btn(pyxel.KEY_DOWN):
            if worldMap[int(self.posX - self.dirX * moveSpeed)][int(self.posY)] == 0:
                self.posX -= self.dirX * moveSpeed
            if worldMap[int(self.posX)][int(self.posY - self.dirY * moveSpeed)] == 0:
                self.posY -= self.dirY * moveSpeed

        #rotatecamera right
        if pyxel.btn(pyxel.KEY_RIGHT):
            oldDirX = self.dirX
            self.dirX = self.dirX * math.cos(-rotSpeed) - self.dirY * math.sin(-rotSpeed)
            self.dirY = oldDirX * math.sin(-rotSpeed) + self.dirY * math.cos(-rotSpeed)

            oldPlaneX = self.planeX
            self.planeX = self.planeX * math.cos(-rotSpeed) - self.planeY * math.sin(-rotSpeed)
            self.planeY = oldPlaneX * math.sin(-rotSpeed) + self.planeY * math.cos(-rotSpeed)

        #rotate camera left
        if pyxel.btn(pyxel.KEY_LEFT):
            oldDirX = self.dirX
            self.dirX = self.dirX * math.cos(rotSpeed) - self.dirY * math.sin(rotSpeed)
            self.dirY = oldDirX * math.sin(rotSpeed) + self.dirY * math.cos(rotSpeed)

            oldPlaneX = self.planeX
            self.planeX = self.planeX * math.cos(rotSpeed) - self.planeY * math.sin(rotSpeed)
            self.planeY = oldPlaneX * math.sin(rotSpeed) + self.planeY * math.cos(rotSpeed)




    def draw(self):
        pyxel.cls(0)

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


App()
