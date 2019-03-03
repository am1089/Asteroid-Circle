import pygame, random, sys, math
from pygame.locals import *

windowWidth = 700
windowHeight = 600
textColor = (0, 0, 255)
backgroundColor = (0, 0, 0)
playerMoveRate = 5
FPS = 40

class variableSize(object):
    def __init__(self, minSize, maxSize, revsPerSec, addRate, image):
        self.minSize = minSize
        self.maxSize = maxSize
        self.revsPerSec = revsPerSec
        self.addRate = addRate
        self.image = image
        self.counter = 0
        self.color = (255,0,0)
        self.list = []
        self.collidedList = []

    def create_add(self):
        self.counter += 1
        if self.counter == self.addRate:
            self.counter = 0
            self.Size = random.randint(self.minSize, self.maxSize)
            self.theta = random.randint(50, 75)
            self.minAngle = random.choice([0, 360])
            if self.minAngle == 360:
                self.maxAngle = 0
            else:
                self.maxAngle = 360
            center_x = windowWidth
            center_y = random.randint(0, windowHeight - self.Size)
            radius = random.randint(75, 100)
            newObject = {'rect': pygame.Rect(center_x,
                                             center_y,
                                             self.Size, self.Size),
                        'surface':pygame.transform.scale(self.image, (self.Size, self.Size)),
                         'theta': self.theta,
                         'center_x': center_x,
                         'center_y': center_y,
                         'radius': radius,
                         'minAngle': self.minAngle,
                         'maxAngle': self.maxAngle
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
            theta = self.revsPerSec * (o['maxAngle'] - o['minAngle']) / FPS
            o['rect'].x = x + o['center_x'] - self.Size/2
            o['rect'].y = y + o['center_y'] - self.Size/2
            theta += o['theta']
            if (theta >= 360):
                theta -= 360
            if (theta <= 0):
                theta += 360
            o['theta'] = theta
            o['center_x'] -= 3
            
    def cullList(self):
        for o in self.collidedList[:]: # collidedlList is were we store collided objects in order for the "enumerate" to not get confused
            self.list.remove(o)
            self.collidedList.remove(o)
        for o in self.list[:]:
            if o['center_x'] + self.Size < 0:
                self.list.remove(o)

    def playerHit(self, playerRect):
        for o in self.list[:]:
            if playerRect.colliderect(o['rect']):
                self.list.remove(o)
                return True
        return False

    def collision(self):
        for i, o1 in enumerate(self.list): # enumerate makes a list of tuples were one part is the index and another part is the value
            for o2 in self.list[i+1:]:
                if o1['rect'].colliderect(o2['rect']):
                    asteroidCollision.play()
                    self.collidedList.append(o1)
                    self.collidedList.append(o2)

        
def terminate():
    pygame.quit()
    sys.exit()

def flipRotation(o):
    if o['minAngle'] == 360:
        o['minAngle'] = 0
        o['maxAngle'] = 360
    else:
        o['minAngle'] = 360
        o['maxAngle'] = 0
    
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
gameOverSound = pygame.mixer.Sound('gameover.wav')
gotHitByAsteroid = pygame.mixer.Sound('0477.wav')
asteroidCollision = pygame.mixer.Sound('explosion.wav')

# Set up images
playerImage = pygame.image.load('player-1.png')
strechedPlayerImage = pygame.transform.scale(playerImage, (40, 40))
playerRect = strechedPlayerImage.get_rect()
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
asteroids = variableSize(30, 40, 0.25, 40, asteroidImage)
while True:
    # Set up the start of the game.
    score = 0
    life = 1
    playerRect.topleft = (windowWidth / 2, windowHeight / 2)
    moveLeft = moveRight = moveUp = moveDown = False
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
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

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * playerMoveRate, 0)
        if moveRight and playerRect.right < windowWidth:
            playerRect.move_ip(playerMoveRate, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * playerMoveRate)
        if moveDown and playerRect.bottom < windowHeight:
            playerRect.move_ip(0, playerMoveRate)

        # Move the asteroids left
        asteroids.moveList()
        
        # Check if Asteroids collided with each other
        asteroids.collision()

        # Draw the game world on the window.
        windowSurface.blit(strechedBackgroundImage, (0, 0))

        # Draw the player's rectangle.
        windowSurface.blit(strechedPlayerImage, playerRect)

        # Draw each asteroid.
        asteroids.drawList()

        #Delete each asteroid
        asteroids.cullList()
        
        pygame.display.update()

        # Check if any of the asteroids have hit the player.
        if asteroids.playerHit(playerRect):
            score -= 10
            life -= 1
            gotHitByAsteroid.play()
            asteroids.list.clear()
            break


        mainClock.tick(FPS)
        

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (windowWidth / 3),
           (windowHeight / 3))
    drawText('Press a key to play again.', font, windowSurface,
           (windowWidth / 3) - 80, (windowHeight / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

gameOverSound.stop()
