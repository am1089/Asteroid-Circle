import pygame, random, sys, math
from pygame.locals import *

windowWidth = 700
windowHeight = 600
textColor = (0, 0, 255)
backgroundColor = (0, 0, 0)
FPS = 40

class variableSize(object):
    def __init__(self, size, revsPerSec, addRate, image):
        self.size = size
        self.revsPerSec = revsPerSec
        self.addRate = addRate
        self.image = image
        self.counter = 0
        self.theta = 90
        self.color = (255,0,0)
        self.list = []

    def create_add(self):
        self.counter += 1
        if self.counter == self.addRate:
            self.counter = 0
            center_x = windowWidth
            center_y = random.randint(0, windowHeight - self.size)
            radius = random.randint(75, 100)
            newObject = {'rect': pygame.Rect(center_x,
                                             center_y,
                                             self.size, self.size),
                        'surface':pygame.transform.scale(self.image, (self.size, self.size)),
                         'theta': self.theta,
                         'center_x': center_x,
                         'center_y': center_y,
                         'radius': radius
            }
            
            self.list.append(newObject)


    def drawList(self):
        for o in self.list[:]:
            windowSurface.blit(o['surface'], o['rect'])

    def moveList(self):
        for o in self.list[:]:
            radians = math.radians(o['theta'])
            x = o['radius'] * math.cos(radians)
            y = o['radius'] * math.sin(radians)
            theta = self.revsPerSec * 360 / FPS
            o['rect'].x = x + o['center_x'] - self.size/2
            o['rect'].y = y + o['center_y'] - self.size/2
            theta += o['theta']
            if (theta >= 360):
                theta -= 360
            o['theta'] = theta
            o['center_x'] -= 3
            
    def cullList(self):
        for o in self.list[:]:
            if o['center_x'] + self.size < 0:
                self.list.remove(o)

    def playerHit(self, playerRect):
        for o in self.list[:]:
            if playerRect.colliderect(o['rect']):
                self.list.remove(o)
                return True
        return False
        
def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, textColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Set up pygame and the window
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Asteroid-Circle')

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
pygame.mixer.music.load('background.mid')

# Set up images
asteroidImage = pygame.image.load('asteroid.png')
backgroundImage = pygame.image.load('8-bit_Space.jpg')
strechedBackgroundImage = pygame.transform.scale(backgroundImage, (windowWidth, windowHeight))

# Show the "Start" screen.
windowSurface.blit(strechedBackgroundImage, (0, 0))
drawText('Asteroid', font, windowSurface, (windowWidth / 3),
       (windowHeight / 3))
drawText('Press a key to start.', font, windowSurface,
       (windowWidth / 3) - 30, (windowHeight / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
asteroids = variableSize(40, 0.25, 60, asteroidImage)
while True:
    # Set up the start of the game.
    score = 0
    life = 1
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

        # Add new asteroid to right of screen
        asteroids.create_add()

        # Move the asteroids left
        asteroids.moveList()
        
        # Draw the game world on the window.
        windowSurface.blit(strechedBackgroundImage, (0, 0))

        # Draw each asteroid.
        asteroids.drawList()

        #Delete each asteroid
        asteroids.cullList()
        
        pygame.display.update()

        mainClock.tick(FPS)
        

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (windowWidth / 3),
           (windowHeight / 3))
    drawText('Press a key to play again.', font, windowSurface,
           (windowWidth / 3) - 80, (windowHeight / 3) + 50)
    player.width = 35
    player.height = 35
    playerMoveRate = 5
    playerStrechedImage = pygame.transform.scale(playerImage, (player.height, player.width))
    pygame.display.update()
    waitForPlayerToPressKey()

gameOverSound.stop()
