import pygame, sys, time, random, math  # import stuff
from pygame.locals import * # 
pygame.mixer.pre_init(44100, 16, 2, 4096)
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

rectText = pygame.image.load('images/tileable2-50px.png')
breakableText = pygame.image.load('images/tileable10-50px.png')
groundText = pygame.image.load('images/ground.png')
houseImage = pygame.image.load('images/house.png')
houseImage = pygame.transform.scale(houseImage, (200, 200))
riverImage = pygame.image.load('images/river.png')
riverImage = pygame.transform.scale(riverImage, (50, 50))

AnimationHeart = []
for i in range(0, 4):
    AnimationHeart.append(pygame.image.load('images/animations/heart_' + str(i) + '.png').convert_alpha())
    AnimationHeart[i] = pygame.transform.scale(AnimationHeart[i], (50, 50))

with open("saveFile.txt") as f:
    availables = f.read().strip().split(sep = ",")

def main():
    # pygame.mixer.music.load("music/airtone_-_brokencloud_1.mp3") # load sounds and music
    pygame.mixer.music.load("music/airtone_-_sleepwalking.mp3") # load sounds and music
    pygame.mixer.music.play(loops=-1, fade_ms=2000)

    with open("saveFile.txt") as f:
        availables = f.read().strip().split(sep = ",")
    
    tom = Tom(*availables)

    rects = []
    enemies = []
    sparkles = []


    tilemap = [ # 0:air 1:block 2: breakable rect 3:enemy 4: sword 5: bracelet 6: house 7:river 8:heart 9:boots 10:boss
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 6, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1, 0, 0, 3, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 6, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 1],
        [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1, 1, 1, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 7, 7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 0, 3, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 1, 1, 1, 1, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 1, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 6, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 7, 7, 7, 1, 1, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 1, 1, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 9, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    rects, enemies, sparkles  = createWorld(tilemap, rects, enemies, sparkles, tom)

    groundX = 0
    groundY = 0

    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

    while True:
        for event in pygame.event.get() :
            if event.type == QUIT :
                saveGame(tom.swordAvailable, tom.braceletAvailable, tom.bootsAvailable)
                pygame.quit()
                sys.exit()
        
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        
        enemies, sparkles, rects = tom.update(enemies, sparkles, rects)

        for i in enemies:
            i.update(rects, tom)
        for i in sparkles:
            i.update()
        for i in rects:
            i.update()

        groundXStart = tom.tomRect.left - tom.limitX
        groundYStart = tom.tomRect.top - tom.limitY
        
        pressed = pygame.key.get_pressed()
        if (pressed[K_ESCAPE]):
            saveGame(tom.swordAvailable, tom.braceletAvailable, tom.bootsAvailable)
            pygame.quit()
            sys.exit()
        
        if (pressed[K_r]):
            reset(tom)
        
        if len(joysticks) <= 0:
            if (pressed[K_SPACE]):
                tom.attack()
            else:
                if (pressed[K_RIGHT]):
                    tom.right(rects, enemies)
                elif (pressed[K_LEFT]):
                    tom.left(rects, enemies)
                if (pressed[K_DOWN]):
                    tom.down(rects, enemies)
                elif (pressed[K_UP]):
                    tom.up(rects, enemies)
        else:
            for joystick in joysticks:
                if joystick.get_button(0):
                    tom.attack()
                else:
                    if joystick.get_axis(0) > 0.1:
                        tom.right(rects, enemies)
                    elif joystick.get_axis(0) < -0.1:
                        tom.left(rects, enemies)
                    if joystick.get_axis(1) > 0.1:
                        tom.down(rects, enemies)
                    elif joystick.get_axis(1) < -0.1:
                        tom.up(rects, enemies)
        
        # display everything
        groundXEnd = tom.tomRect.left - tom.limitX
        groundYEnd = tom.tomRect.top - tom.limitY

        groundX += groundXEnd - groundXStart 
        groundY += groundYEnd - groundYStart 
        if groundX  <= -groundText.get_width() or groundX >= groundText.get_width():
            groundX = 0
        if groundY  <= -groundText.get_width() or groundY >= groundText.get_width():
            groundY = 0
        paint(pygame.Rect(-groundX - groundText.get_width() * 1.5, -groundY - groundText.get_height() * 1.5, 800 + groundText.get_width() * 3, 800 + groundText.get_height() * 3), groundText)


        for i in rects:
            i.draw(tom)
        
        for i in enemies:
            i.draw(tom)

        for i in sparkles:
            i.draw(tom)

        tom.draw()

        pygame.display.update()
        fpsClock.tick(FPS)

class Tom:
    def __init__(self, swordAvailable, braceletAvailable, bootsAvailable):

        self.AnimationWalkDown = []
        for i in range(0, 4):
            self.AnimationWalkDown.append(pygame.image.load('images/animations/walk_forward_' + str(i) + '.png').convert_alpha())
            self.AnimationWalkDown[i] = pygame.transform.scale(self.AnimationWalkDown[i], (60, 90))
        
        self.AnimationWalkRight = []
        for i in range(0, 4):
            self.AnimationWalkRight.append(pygame.image.load('images/animations/walk_right_' + str(i) + '.png').convert_alpha())
            self.AnimationWalkRight[i] = pygame.transform.scale(self.AnimationWalkRight[i], (60, 90))
        
        self.AnimationWalkUp = []
        for i in range(0, 4):
            self.AnimationWalkUp.append(pygame.image.load('images/animations/walk_up_' + str(i) + '.png').convert_alpha())
            self.AnimationWalkUp[i] = pygame.transform.scale(self.AnimationWalkUp[i], (60, 90))
        
        self.AnimationWalkLeft = []
        for i in range(0, 4):
            self.AnimationWalkLeft.append(pygame.image.load('images/animations/walk_left_' + str(i) + '.png').convert_alpha())
            self.AnimationWalkLeft[i] = pygame.transform.scale(self.AnimationWalkLeft[i], (60, 90))
        



        self.AnimationAttackDown = []
        for i in range(0, 4):
            self.AnimationAttackDown.append(pygame.image.load('images/animations/attack_down_' + str(i) + '.png').convert_alpha())
            self.AnimationAttackDown[i] = pygame.transform.scale(self.AnimationAttackDown[i], (60, 90))
        
        self.AnimationAttackUp = []
        for i in range(0, 4):
            self.AnimationAttackUp.append(pygame.image.load('images/animations/attack_up_' + str(i) + '.png').convert_alpha())
            self.AnimationAttackUp[i] = pygame.transform.scale(self.AnimationAttackUp[i], (60, 90))
        
        self.AnimationAttackRight = []
        for i in range(0, 4):
            self.AnimationAttackRight.append(pygame.image.load('images/animations/attack_right_' + str(i) + '.png').convert_alpha())
            self.AnimationAttackRight[i] = pygame.transform.scale(self.AnimationAttackRight[i], (60, 90))

        self.AnimationAttackLeft = []
        for i in range(0, 4):
            self.AnimationAttackLeft.append(pygame.image.load('images/animations/attack_left_' + str(i) + '.png').convert_alpha())
            self.AnimationAttackLeft[i] = pygame.transform.scale(self.AnimationAttackLeft[i], (60, 90))

        self.tomRect = self.AnimationWalkDown[0].get_rect()

        self.hearttext = pygame.image.load('images/Heart.png').convert_alpha()
        self.hearttext = pygame.transform.scale(self.hearttext, (50, 50))
        self.heartgreytext = pygame.image.load('images/Heartgrey.png').convert_alpha()
        self.heartgreytext = pygame.transform.scale(self.heartgreytext, (50, 50))

        self.attackSound = pygame.mixer.Sound("music/swish-1.wav")
        self.hurtSound = pygame.mixer.Sound("music/deathh.wav")
        self.deathSound = pygame.mixer.Sound("music/Deathsound.mp3")
        self.enemyDeathSound = pygame.mixer.Sound("music/paind.wav")
        self.foundSound = pygame.mixer.Sound("music/chipquest.wav")
        self.breakSound = pygame.mixer.Sound("music/rock_break.ogg")
        self.healSound = pygame.mixer.Sound("music/healspell1.aif")

        self.limitX = 400 - self.tomRect.width / 2
        self.limitY = 400 - self.tomRect.height / 2

        self.tomRect.left = self.limitX
        self.tomRect.top = self.limitY

        self.AnimationWalkTimer = 0
        self.AnimationAttackTimer = 0

        self.movingDown = False
        self.movingUp = False
        self.movingRight = False
        self.movingLeft = False

        self.moveLast = "d"

        self.speed = math.floor(150 * 1/FPS)

        self.attacking = False
        self.attackBox = pygame.Rect(-1000, -1000, self.tomRect.width, self.tomRect.height)
        self.range = 40

        self.maxHealth = 3
        self.health = self.maxHealth
        self.houseOnce = False
        self.collisionHouse = False

        self.hurtOnce = False
        self.collisionEnemy = False

        self.attackBossOnce = False
        self.collisionBoss = False

        if swordAvailable == "True":
            self.swordAvailable = True
        else:
            self.swordAvailable = False

        if braceletAvailable == "True":
            self.braceletAvailable = True
        else:
            self.braceletAvailable = False

        if bootsAvailable == "True":
            self.bootsAvailable = True
        else:
            self.bootsAvailable = False

        self.dead = False
    
    def update(self, enemies, sparkles, rects):
        self.AnimationWalkTimer += 1/FPS * 7
        if self.AnimationWalkTimer >= 4:
            self.AnimationWalkTimer = 0
        
        if self.attacking:
            self.AnimationAttackTimer += 1/FPS * 7
            if self.AnimationAttackTimer >= 4:
                self.AnimationAttackTimer = 0
                self.attacking = False
        
        self.movingDown = False
        self.movingUp = False
        self.movingRight = False
        self.movingLeft = False

        self.collisionEnemy = False
        self.collisionBoss = False
        for i in enemies:
            if self.tomRect.colliderect(i.hitbox):
                if not self.hurtOnce:
                    self.hurt()
                    self.hurtOnce = True
                self.collisionEnemy = True
            
            if self.attacking:
                if self.attackBox.colliderect(i.hitbox):
                    if i.boss:
                        if not self.attackBossOnce:
                            self.enemyDeathSound.play()
                            i.health -= 1
                            self.attackBossOnce = True
                            if i.health <= 0:
                                enemies.remove(i)
                                self.finish()
                        self.collisionBoss = True
                    else:
                        enemies.remove(i)
                        self.enemyDeathSound.play()
                
        if not self.collisionEnemy:
            self.hurtOnce = False
        if not self.collisionBoss:
            self.attackBossOnce = False
        
        self.collisionHouse = False

        if self.attacking:
            if self.braceletAvailable:
                for i in rects:
                    if self.attackBox.colliderect(i.rect) and i.breakable:
                        rects.remove(i)
                        self.breakSound.play()
            
            for i in rects:
                if self.attackBox.colliderect(i.rect) and i.house and i.heartsAvailable > 0:
                    if not self.houseOnce:
                        self.healSound.play()
                        i.heartsAvailable -= 1
                        rects.append(Object(*i.rect.midbottom, 50, 50, heart=True))
                        self.houseOnce = True
                    self.collisionHouse = True

                if self.attackBox.colliderect(i.rect) and i.heart:
                    if self.health < self.maxHealth:
                        rects.remove(i)
                        self.health += 1
                        self.healSound.play()

        if not self.collisionHouse:
            self.houseOnce = False
        
        sparkleIndex = self.tomRect.collidelist(sparkles)

        if not sparkleIndex == -1:
            match sparkles[sparkleIndex].type:
                case "sword":
                    self.swordAvailable = True
                    font = pygame.font.SysFont(None, 50)
                    img = font.render("You Found Your Sword!", True, BLACK)
                    WINDOW.blit(img, (200, 200))
                    img = font.render("Attack with space!", True, BLACK)
                    WINDOW.blit(img, (200, 300))
                    pygame.display.update()
                case "bracelet":
                    self.braceletAvailable = True
                    font = pygame.font.SysFont(None, 50)
                    img = font.render("You Found The Bracelet Of Power!", True, BLACK)
                    WINDOW.blit(img, (200, 200))
                    img = font.render("Break rocks with your sword!", True, BLACK)
                    WINDOW.blit(img, (200, 300))
                    pygame.display.update()
                case "boots":
                    self.bootsAvailable = True
                    font = pygame.font.SysFont(None, 50)
                    img = font.render("You Found The Boots Of WaterWalking!", True, BLACK)
                    WINDOW.blit(img, (100, 200))
                    img = font.render("Walk across water!", True, BLACK)
                    WINDOW.blit(img, (200, 300))
                    pygame.display.update()
            saveGame(self.swordAvailable, self.braceletAvailable, self.bootsAvailable)
            self.foundSound.play()
            time.sleep(3)
            sparkles.remove(sparkles[sparkleIndex])

        

        if self.health <= 0:
            self.death()
        
        return enemies, sparkles, rects
    
    def draw(self):
        if not self.attacking:
            if self.movingDown:
                WINDOW.blit(self.AnimationWalkDown[math.floor(self.AnimationWalkTimer)], (self.limitX, self.limitY))
            elif self.movingRight:
                WINDOW.blit(self.AnimationWalkRight[math.floor(self.AnimationWalkTimer)], (self.limitX, self.limitY))
            elif self.movingUp:
                WINDOW.blit(self.AnimationWalkUp[math.floor(self.AnimationWalkTimer)], (self.limitX, self.limitY))
            elif self.movingLeft:
                WINDOW.blit(self.AnimationWalkLeft[math.floor(self.AnimationWalkTimer)], (self.limitX, self.limitY))
            else:
                match self.moveLast:
                    case "d":
                        WINDOW.blit(self.AnimationWalkDown[0], (self.limitX, self.limitY))
                    case "u":
                        WINDOW.blit(self.AnimationWalkUp[0], (self.limitX, self.limitY))
                    case "r":
                        WINDOW.blit(self.AnimationWalkRight[0], (self.limitX, self.limitY))
                    case "l":
                        WINDOW.blit(self.AnimationWalkLeft[0], (self.limitX, self.limitY))
        else:
            match self.moveLast:
                case "d":
                    WINDOW.blit(self.AnimationAttackDown[math.floor(self.AnimationAttackTimer)], (self.limitX, self.limitY))
                case "u":
                    WINDOW.blit(self.AnimationAttackUp[math.floor(self.AnimationAttackTimer)], (self.limitX, self.limitY))
                case "r":
                    WINDOW.blit(self.AnimationAttackRight[math.floor(self.AnimationAttackTimer)], (self.limitX, self.limitY))
                case "l":
                    WINDOW.blit(self.AnimationAttackLeft[math.floor(self.AnimationAttackTimer)], (self.limitX, self.limitY))
        
        self.hearts()

    def right(self, rects, enemies):
        self.movingRight = True
        self.tomRect.move_ip(self.speed, 0)
        self.moveLast = "r"
        allowed = True
        for i in rects:
            if not i.heart:
                if self.bootsAvailable:
                    if not i.river:
                        if self.tomRect.colliderect(i.rect) or self.tomRect.collidelist(enemies) != -1:
                            allowed = False
                else:
                    if self.tomRect.colliderect(i.rect) or self.tomRect.collidelist(enemies) != -1:
                        allowed = False
        if not allowed:
            self.tomRect.move_ip(-self.speed, 0)
    
    def left(self, rects, enemies):
        self.movingLeft = True
        self.tomRect.move_ip(-self.speed, 0)
        self.moveLast = "l"
        allowed = True
        for i in rects:
            if not i.heart:
                if self.bootsAvailable:
                    if not i.river:
                        if self.tomRect.colliderect(i.rect) or self.tomRect.collidelist(enemies) != -1:
                            allowed = False
                else:
                    if self.tomRect.colliderect(i.rect) or self.tomRect.collidelist(enemies) != -1:
                        allowed = False
        if not allowed:
            self.tomRect.move_ip(self.speed, 0)
            
    def down(self, rects, enemies):        
        self.movingDown = True
        self.moveLast = "d"
        self.tomRect.move_ip(0, self.speed)
        allowed = True
        for i in rects:
            if not i.heart:
                if self.bootsAvailable:
                    if not i.river:
                        if self.tomRect.colliderect(i.rect) or self.tomRect.collidelist(enemies) != -1:
                            allowed = False
                else:
                    if self.tomRect.colliderect(i.rect) or self.tomRect.collidelist(enemies) != -1:
                        allowed = False
        if not allowed:
            self.tomRect.move_ip(0, -self.speed)

    def up(self, rects, enemies):
        self.movingUp = True
        self.tomRect.move_ip(0, -self.speed)
        self.moveLast = "u"
        allowed = True
        for i in rects:
            if not i.heart:
                if self.bootsAvailable:
                    if not i.river:
                        if self.tomRect.colliderect(i.rect) or self.tomRect.collidelist(enemies) != -1:
                            allowed = False
                else:
                    if self.tomRect.colliderect(i.rect) or self.tomRect.collidelist(enemies) != -1:
                        allowed = False
        if not allowed:
            self.tomRect.move_ip(0, self.speed)
    
    def attack(self):
        if self.swordAvailable and not self.attacking:
            self.attacking = True
            self.attackSound.play()
            match self.moveLast:
                case "d":
                    self.attackBox.left = self.tomRect.left
                    self.attackBox.top = self.tomRect.top + self.range
                case "u":
                    self.attackBox.left = self.tomRect.left
                    self.attackBox.top = self.tomRect.top - self.range
                case "r":
                    self.attackBox.left = self.tomRect.left + self.range
                    self.attackBox.top = self.tomRect.top
                case "l":
                    self.attackBox.left = self.tomRect.left - self.range
                    self.attackBox.top = self.tomRect.top
    
    def hearts(self):
        for i in range(0, self.maxHealth):
            if i < self.health:
                WINDOW.blit(self.hearttext, (i * 50, 0))
            else:
                WINDOW.blit(self.heartgreytext, (i * 50, 0))
    
    def hurt(self):
        self.health -= 1
        self.hurtSound.play()
    
    def death(self):
        self.deathSound.play()
        self.dead = True
        time.sleep(2)
        pygame.quit()
        sys.exit()
    
    def finish(self):
        font = pygame.font.SysFont(None, 50)
        img = font.render("You Beat The Game!", True, BLACK)
        WINDOW.blit(img, (100, 200))
        pygame.display.update()
        saveGame(self.swordAvailable, self.braceletAvailable, self.bootsAvailable)
        self.foundSound.play()
        time.sleep(3)
        pygame.quit()
        sys.exit()
        



class Object:
    def __init__(self, x, y, w, h, breakable=False, house=False, river=False, heart=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.breakable = breakable
        self.house = house
        self.river = river
        self.heart = heart
        self.heartsAvailable = 1
        self.timer = 0
    
    def update(self):
        self.timer += 1/FPS * 7
        if self.timer >= 4:
            self.timer = 0
    
    def draw(self, tom):
        if (0 - self.rect.width) < self.rect.left - tom.tomRect.left + tom.limitX < WINDOW_WIDTH and (0 - self.rect.height) < self.rect.top - tom.tomRect.top + tom.limitY < WINDOW_HEIGHT:
            if self.breakable:
                WINDOW.blit(breakableText, (self.rect.left - tom.tomRect.left + tom.limitX,
                                    self.rect.top - tom.tomRect.top + tom.limitY,
                                    self.rect.width,
                                    self.rect.height))
            elif self.house:
                WINDOW.blit(houseImage, (self.rect.left - tom.tomRect.left + tom.limitX,
                                    self.rect.top - tom.tomRect.top + tom.limitY,))
            elif self.river:
                WINDOW.blit(riverImage, (self.rect.left - tom.tomRect.left + tom.limitX,
                                    self.rect.top - tom.tomRect.top + tom.limitY,))
            elif self.heart:
                WINDOW.blit(AnimationHeart[math.floor(self.timer)], (self.rect.left - tom.tomRect.left + tom.limitX,
                                    self.rect.top - tom.tomRect.top + tom.limitY,))
            else:
                WINDOW.blit(rectText, (self.rect.left - tom.tomRect.left + tom.limitX,
                                        self.rect.top - tom.tomRect.top + tom.limitY,
                                        self.rect.width,
                                        self.rect.height))



class Enemy:
    def __init__(self, x, y, w, h, boss=False):
        self.image = pygame.image.load('images/enemy_walk_1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.imageRight = pygame.transform.flip(self.image, True, False)
        self.rect.left = x
        self.rect.top = y
        self.hitbox = pygame.Rect(x - 5, y - 5, w + 10, h + 10)

        self.movingDown = False
        self.movingUp = False
        self.movingRight = False
        self.movingLeft = False

        self.boss = boss

        if self.boss:
            self.health = 10
            self.image = pygame.image.load('images/enemyBoss.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (w, h))
            self.imageRight = pygame.transform.flip(self.image, True, False)
            self.speed = 50 / FPS
        else:
            self.speed = 30 / FPS
    
    def update(self, rects, tom):
        if (0 - self.rect.width) < self.rect.left - tom.tomRect.left + tom.limitX < WINDOW_WIDTH and (0 - self.rect.height) < self.rect.top - tom.tomRect.top + tom.limitY < WINDOW_HEIGHT:
            if not self.boss:
                n = random.randint(0, 20)
                if n == 1:
                    self.movingDown = not self.movingDown
                if n == 2:
                    self.movingUp = not self.movingUp
                if n == 3:
                    self.movingRight = not self.movingRight
                if n == 4:
                    self.movingLeft = not self.movingLeft
            else:
                if tom.tomRect.left <= self.rect.left:
                    self.movingLeft = True
                    self.movingRight = False
                else:
                    self.movingRight = True
                    self.movingLeft = False
                if tom.tomRect.top <= self.rect.top:
                    self.movingUp = True
                    self.movingDown = False
                else:
                    self.movingDown = True
                    self.movingUp = False
            
            if self.boss and self.speed > (tom.tomRect.top - self.rect.top) > -self.speed:

                if self.movingDown and self.speed > (tom.tomRect.top - self.rect.top):
                    self.rect = self.rect.move(0, tom.tomRect.top - self.rect.top)

                elif self.movingUp and (tom.tomRect.top - self.rect.top) < -self.speed:
                    self.rect = self.rect.move(0, tom.tomRect.top - self.rect.top)
            
            else:
                if self.movingDown:
                    self.rect = self.rect.move(0, self.speed)
                if self.movingUp:
                    self.rect = self.rect.move(0, -self.speed)



            if self.boss and self.speed > (tom.tomRect.left - self.rect.left) > -self.speed:

                if self.movingRight and self.speed > (tom.tomRect.left - self.rect.left):
                    self.rect = self.rect.move(tom.tomRect.top - self.rect.top, 0)

                elif self.movingLeft and (tom.tomRect.left - self.rect.left) < -self.speed:
                    self.rect = self.rect.move(tom.tomRect.top - self.rect.top, 0)
                print("aaaaa")
            
            else:
                if self.movingRight:
                    self.rect = self.rect.move(self.speed, 0)
                if self.movingLeft:
                    self.rect = self.rect.move(-self.speed, 0)

            self.hitbox.left = self.rect.left - 5
            self.hitbox.top = self.rect.top - 5

            allowed = True

            for i in rects:
                if self.rect.colliderect(i.rect):
                    allowed = False
            if self.rect.colliderect(tom.tomRect):
                    allowed = False
            if not allowed:
                if self.movingDown:
                    self.rect = self.rect.move(0, -self.speed)
                if self.movingUp:
                    self.rect = self.rect.move(0, self.speed)
                if self.movingRight:
                    self.rect = self.rect.move(-self.speed, 0)
                if self.movingLeft:
                    self.rect = self.rect.move(self.speed, 0)

    def draw(self, tom):
        if (0 - self.rect.width) < self.rect.left - tom.tomRect.left + tom.limitX < WINDOW_WIDTH and (0 - self.rect.height) < self.rect.top - tom.tomRect.top + tom.limitY < WINDOW_HEIGHT:
            if self.movingLeft:
                WINDOW.blit(self.image, (self.rect.left - tom.tomRect.left + tom.limitX,
                                        self.rect.top - tom.tomRect.top + tom.limitY)) 
            else:
                WINDOW.blit(self.imageRight, (self.rect.left - tom.tomRect.left + tom.limitX,
                                        self.rect.top - tom.tomRect.top + tom.limitY)) 


class Sparkle:
    def __init__(self, x, y, type):
        self.type = type
        self.sparkleFrames = []
        for i in range(0, 4):
            self.sparkleFrames.append(pygame.image.load('images/animations/sparkle_' + str(i) + '.png').convert_alpha())
            self.sparkleFrames[i] = pygame.transform.scale(self.sparkleFrames[i], (50, 50))
        self.rect = self.sparkleFrames[0].get_rect()
        self.rect.left = x
        self.rect.top = y
        self.timer = 0
    
    def update(self):
        self.timer += 6 * 1/FPS
        if self.timer >= 4:
            self.timer = 0
    
    def draw(self, tom):
        if (0 - self.rect.width) < self.rect.left - tom.tomRect.left + tom.limitX < WINDOW_WIDTH and (0 - self.rect.height) < self.rect.top - tom.tomRect.top + tom.limitY < WINDOW_HEIGHT:
            WINDOW.blit(self.sparkleFrames[math.floor(self.timer)], 
                        (self.rect.left - tom.tomRect.left + tom.limitX,
                        self.rect.top - tom.tomRect.top + tom.limitY))

          


def createWorld(tilemap, rects, enemies, sparkles, tom):
    size = 50
    for y in range(len(tilemap)):
        for x in range(len(tilemap[y])):
            if tilemap[y][x] == 1:
                rects.append(Object(x * size, y * size, size, size, False))
            if tilemap[y][x] == 2:
                rects.append(Object(x * size, y * size, size, size, True))
            if tilemap[y][x] == 3:
                enemies.append(Enemy(x * size, y * size, size, size))
            if tilemap[y][x] == 4:
                if not tom.swordAvailable:
                    sparkles.append(Sparkle(x * size, y * size, "sword"))
            if tilemap[y][x] == 5:
                if not tom.braceletAvailable:
                    sparkles.append(Sparkle(x * size, y * size, "bracelet"))
            if tilemap[y][x] == 6:
                rects.append(Object(x * size, y * size, 200, 200, False, True))
            if tilemap[y][x] == 7:
                rects.append(Object(x * size, y * size, size, size, river=True))
            if tilemap[y][x] == 8:
                rects.append(Object(x * size, y * size, size, size, heart=True))
            if tilemap[y][x] == 9:
                if not tom.bootsAvailable:
                    sparkles.append(Sparkle(x * size, y * size, "boots"))
            if tilemap[y][x] == 10:
                enemies.append(Enemy(x * size, y * size, size * 3, size * 3, True))
    return rects, enemies, sparkles

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

def saveGame(sword, bracelet, boots):
    with open("saveFile.txt", "w") as f:
        f.write(str(sword) + "," + str(bracelet) + "," + str(boots))

def reset(tom):
    with open("saveFile.txt", "w") as f:
        f.write("False,False,False")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()