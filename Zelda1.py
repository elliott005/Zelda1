import pygame, sys, time, random, math  # import stuff
from pygame.locals import * # 
pygame.init() # initialise pygame

BACKGROUND = (120, 100, 255) # initialise colors
RED = (255, 30, 70)
BLUE = (10, 20, 200)
GREEN = (50, 230, 40)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
STARMODE = (255, 189, 0)

FPS = 25
fpsClock = pygame.time.Clock() # init screen and fps
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Zelda!')

def main():
    pygame.mixer.music.load("music/airtone_-_sleepwalking.mp3") # load sounds and music
    pygame.mixer.music.play(loops=-1, fade_ms=2000)

    rectText = pygame.image.load('images/tileable2-50px.png')
    groundText = pygame.image.load('images/ground.png')

    tom = Tom()

    rects = []


    tilemap = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    ]

    rects = createWorld(tilemap, rects)

    groundX = 0
    groundY = 0

    while True:
        for event in pygame.event.get() :
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
        
        tom.update()

        groundXStart = tom.tomRect.left - tom.limitX
        groundYStart = tom.tomRect.top - tom.limitY
        
        pressed = pygame.key.get_pressed()
        if (pressed[K_ESCAPE]):
            pygame.quit()
            sys.exit()
        
        if (pressed[K_RIGHT]):
            tom.right(rects)
        elif (pressed[K_LEFT]):
            tom.left(rects)
        if (pressed[K_DOWN]):
            tom.down(rects)
        elif (pressed[K_UP]):
            tom.up(rects)
        
        WINDOW.fill(BACKGROUND) # display everything
        groundXEnd = tom.tomRect.left - tom.limitX
        groundYEnd = tom.tomRect.top - tom.limitY

        groundX += groundXEnd - groundXStart 
        groundY += groundYEnd - groundYStart 
        if groundX  <= -groundText.get_width() or groundX >= groundText.get_width():
            groundX = 0
        if groundY  <= -groundText.get_width() or groundY >= groundText.get_width():
            groundY = 0
        paint(pygame.Rect(-groundX - groundText.get_width() * 1.5, -groundY - groundText.get_height() * 1.5, 800 + groundText.get_width() * 3, 800 + groundText.get_height() * 3), groundText)

        tom.draw()

        for i in rects:
            WINDOW.blit(rectText, (i.left - tom.tomRect.left + tom.limitX,
                                i.top - tom.tomRect.top + tom.limitY,
                                i.width,
                                i.height))

        pygame.display.update()
        fpsClock.tick(FPS)

class Tom:
    def __init__(self):
        self.animationDown = []
        for i in range(0, 4):
            self.animationDown.append(pygame.image.load('images/animations/walk_forward_' + str(i) + '.png').convert_alpha())
            self.animationDown[i] = pygame.transform.scale(self.animationDown[i], (60, 90))
        
        self.animationRight = []
        for i in range(0, 4):
            self.animationRight.append(pygame.image.load('images/animations/walk_right_' + str(i) + '.png').convert_alpha())
            self.animationRight[i] = pygame.transform.scale(self.animationRight[i], (60, 90))
        
        self.animationUp = []
        for i in range(0, 4):
            self.animationUp.append(pygame.image.load('images/animations/walk_up_' + str(i) + '.png').convert_alpha())
            self.animationUp[i] = pygame.transform.scale(self.animationUp[i], (60, 90))
        
        self.animationLeft = []
        for i in range(0, 4):
            self.animationLeft.append(pygame.image.load('images/animations/walk_left_' + str(i) + '.png').convert_alpha())
            self.animationLeft[i] = pygame.transform.scale(self.animationLeft[i], (60, 90))

        self.tomRect = self.animationDown[0].get_rect()

        self.limitX = 400 - self.tomRect.width / 2
        self.limitY = 400 - self.tomRect.height / 2

        self.tomRect.left = self.limitX
        self.tomRect.top = self.limitY

        self.animationTimer = 0

        self.movingDown = False
        self.movingUp = False
        self.movingRight = False
        self.movingLeft = False

        self.moveLast = "d"
    
    def update(self):
        self.animationTimer += 1/FPS * 7
        if self.animationTimer >= 4:
            self.animationTimer = 0
        
        self.movingDown = False
        self.movingUp = False
        self.movingRight = False
        self.movingLeft = False
    
    def draw(self):
        if self.movingDown:
            WINDOW.blit(self.animationDown[math.floor(self.animationTimer)], (self.limitX, self.limitY))
        elif self.movingRight:
            WINDOW.blit(self.animationRight[math.floor(self.animationTimer)], (self.limitX, self.limitY))
        elif self.movingUp:
            WINDOW.blit(self.animationUp[math.floor(self.animationTimer)], (self.limitX, self.limitY))
        elif self.movingLeft:
            WINDOW.blit(self.animationLeft[math.floor(self.animationTimer)], (self.limitX, self.limitY))
        else:
            match self.moveLast:
                case "d":
                    WINDOW.blit(self.animationDown[0], (self.limitX, self.limitY))
                case "u":
                    WINDOW.blit(self.animationUp[0], (self.limitX, self.limitY))
                case "r":
                    WINDOW.blit(self.animationRight[0], (self.limitX, self.limitY))
                case "l":
                    WINDOW.blit(self.animationLeft[0], (self.limitX, self.limitY))

    def right(self, rects):
        if pygame.Rect(self.tomRect.left + 100 * 1/FPS, self.tomRect.top, self.tomRect.width, self.tomRect.height).collidelist(rects) == -1:
            self.movingRight = True
            self.tomRect.move_ip(100 * 1/FPS, 0)
        self.moveLast = "r"
    
    def left(self, rects):
        if pygame.Rect(self.tomRect.left - 100 * 1/FPS, self.tomRect.top, self.tomRect.width, self.tomRect.height).collidelist(rects) == -1:
            self.movingLeft = True
            self.tomRect.move_ip(-(100 * 1/FPS), 0)
        self.moveLast = "l"

    def down(self, rects):
        if pygame.Rect(self.tomRect.left, self.tomRect.top + 100 * 1/FPS, self.tomRect.width, self.tomRect.height).collidelist(rects) == -1:
            self.movingDown = True
            self.tomRect.move_ip(0, 100 * 1/FPS)
        self.moveLast = "d"

    def up(self, rects):
        if pygame.Rect(self.tomRect.left, self.tomRect.top - 100 * 1/FPS, self.tomRect.width, self.tomRect.height).collidelist(rects) == -1:
            self.movingUp = True
            self.tomRect.move_ip(0, -(100 * 1/FPS))
        self.moveLast = "u"

def createWorld(tilemap, rects):
    size = 50
    for y in range(len(tilemap)):
        for x in range(len(tilemap[y])):
            if tilemap[y][x] == 1:
                rects.append(pygame.Rect(x * size, y * size, size, size))
    return rects

def paint (forme, texture):
    for x in range(0, forme.width, texture.get_width()):
        for y in range(0, forme.height, texture.get_height()):
            WINDOW.blit(
                texture,
                (forme.left + x, forme.top + y),
                Rect(
                    0,
                    0,
                    forme.right - (forme.left + x),
                    forme.bottom - (forme.top + y)
                )
            )

if __name__ == "__main__":
    main()