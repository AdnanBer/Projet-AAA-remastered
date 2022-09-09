import pygame, sys
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
mainClock = pygame.time.Clock()

import pygame
file = 'sons/musique.wav'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play(-1) # If the loops is -1 then the music will repeat indefinitely.



# taille écran et fenêtre
SIZE = 20
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 60
G = 0.3
F = 0.9
J = 6
S = 5
MAXS = 9
epsilon = 0.1

# touches affiliées aux commandes du personnage
keys = pygame.key.get_pressed()

# initialisation de la fenêtre
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

# titre de la fenêtre
pygame.display.set_caption('Grumble')

# police du titre
basicFont = pygame.font.SysFont("Comic Sans MS", 60)

# couleurs présentes dans le titre de la fenêtre
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (127, 127, 127)


# création des classes

class Character:

    def __init__(self, x, y):

        self.dx = 0  # vitesse du personnage
        self.dy = 0

        self.image = pygame.image.load("jeu/persoRight.bmp").convert()  # charger l'image du joueur
        self.image.set_colorkey(GREY)  # affilier la couleur grise au transparent

        self.rect = self.image.get_rect()  # créer une hitbox rectangulaire autour du perso
        self.rect.left = x
        self.rect.bottom = y
        self.win = True
        self.coins = 0
        self.coinSound = pygame.mixer.Sound('sons/coin.wav')
        self.allCoins = False

        self.dead = False
        self.deadSound = pygame.mixer.Sound('sons/dead.wav')
        self.touchGround = True
        self.lives = 5

        self.imageLives = pygame.image.load("jeu/lives.bmp").convert()
        self.imageLives.set_colorkey(GREY)

        self.imageCoins = pygame.image.load("jeu/coin.bmp").convert()
        self.imageCoins.set_colorkey(GREY)

        self.imageCross = pygame.image.load("jeu/x.bmp").convert()
        self.imageCross.set_colorkey(GREY)

        self.imageNumberOfCoins = pygame.image.load("jeu/2.bmp").convert()
        self.imageNumberOfCoins.set_colorkey(GREY)

        self.jumpSound = pygame.mixer.Sound('sons/jump.wav')

    def move(self, collisionList):

        # déplacer le personnage après que les méthodes move aient été utilisées
        self.grav()
        # self.friction()

        self.rect.x += self.dx
        self.collisionX(collisionList)

        self.rect.y += self.dy
        self.collisionY(collisionList)

        if self.dead:
            self.lives += -1

    def moveRight(self):

        # déplacer le personnage vers la droite ainsi que l'image qui lui est affiliée

        self.dx = S

    def moveLeft(self):

        # déplacer le personnage vers la gauche ainsi que l'image qui lui est affiliée
        self.dx = -S

    def jump(self, collisionList):

        # vérifier le sol afi de calibrer le saut du personnage
        self.rect.y += 1
        if self.rect.bottom >= WINDOWHEIGHT:  # sol bas
            self.rect.bottom = WINDOWHEIGHT - 1  # collision(self) implique self.y = 580 if self.y >= 580
            self.dy = -J  # vitesse dde saut
            self.jumpSound.play()
        else:
            for c in collisionList:
                if c[1] == 't':
                    if c[0].rect.colliderect(self.rect):
                        self.rect.bottom = c[0].rect.top - 1
                        self.dy = -J
                        self.jumpSound.play()
        self.rect.y -= 1

    def stop(self):

        # arrêter le le déplacement du personnage sur les côtés
        char.dx = 0

    def grav(self):

        # création d'une gravité dans le jeu
        self.dy += G

        if self.dy <= -MAXS:
            self.dy = -MAXS
        elif self.dy >= MAXS:
            self.dy = MAXS

        if self.rect.bottom >= WINDOWHEIGHT and self.dy >= 0:
            self.dy = 0
            self.rect.bottom = WINDOWHEIGHT

    def friction(self):

        # applique une certaine friction du personnage sur les éléments du jeu
        self.dy = self.dy * F
        self.dx = self.dx * F

    def collisionX(self, level):

        for c in level.collisionList:
            if c[0].rect.colliderect(self.rect):
                if c[1] == 't':
                    if self.dx > 0:
                        self.rect.right = c[0].rect.left
                    elif self.dx < 0:
                        self.rect.left = c[0].rect.right
                if c[1] == 'd':
                    if self.allCoins:
                        self.win = True
                if c[1] == 'm':
                    c[0].sound.play()
                    self.dy = -1.5 * J
                if c[1] == 'c':
                    self.coinSound.play()
                    level.collisionList.remove(c)
                    self.addCoin(level.numberOfCoins)
                if c[1] == 's':
                    self.dead = True
                    char.deadSound.play()

        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WINDOWWIDTH:
            self.rect.right = WINDOWWIDTH

    def collisionY(self, level):

        # vérifie la position et le déplacement du personnage
        for c in level.collisionList:
            if c[0].rect.colliderect(self.rect):
                if c[1] == 't':
                    if self.dy > 0:
                        self.rect.bottom = c[0].rect.top
                        self.dy = 0
                    if self.dy < 0:
                        self.rect.top = c[0].rect.bottom
                        self.dy = 0
                if c[1] == 'd':
                    if self.allCoins:
                        self.win = True
                if c[1] == 'm':
                    self.dy = -1.5 * J
                    c[0].sound.play()
                if c[1] == 'c':
                    self.coinSound.play()
                    level.collisionList.remove(c)
                    self.addCoin(level.numberOfCoins)
                if c[1] == 's':
                    self.dead = True
                    char.deadSound.play()

    def draw(self):
        if self.touchGround:
            if self.dx > 0:
                self.image = pygame.image.load("jeu/persoRight.bmp")
                self.image.set_colorkey(GREY)
            elif self.dx < 0:
                self.image = pygame.image.load("jeu/persoLeft.bmp")
                self.image.set_colorkey(GREY)

        for i in range(self.lives - 1):
            windowSurface.blit(self.imageLives, ((i + 2) * SIZE, 1.5 * SIZE))

        windowSurface.blit(self.imageCoins, (2 * SIZE, SIZE * 3))
        windowSurface.blit(self.imageCross, (3 * SIZE, SIZE * 3))
        windowSurface.blit(self.imageNumberOfCoins, (4 * SIZE, SIZE * 3))

        windowSurface.blit(self.image, self.rect)  # fait apparaître le personnage à la surface

    def addCoin(self, numberOfCoins):
        self.coins += 1
        if self.coins == numberOfCoins:
            self.allCoins = True
            self.coins = 0


class Stuff:

    def __init__(self, X, Y, stuffName):
        self.X = X
        self.Y = Y
        self.stuffName = stuffName
        self.image = pygame.image.load('jeu/' + self.stuffName + ".bmp")
        self.image.set_colorkey(GREY)  # cette commande permet de rendre le détourage gris en transparent
        self.rect = self.image.get_rect()  # créer le rectangle associé avec la plateforme
        self.rect.left = SIZE * self.X
        self.rect.bottom = SIZE * (self.Y + 1)

    def draw(self):
        windowSurface.blit(self.image, self.rect)


class Platform(Stuff):

    def __init__(self, X, Y):
        Stuff.__init__(self, X, Y, "platform")


class Door(Stuff):

    def __init__(self, X, Y):
        Stuff.__init__(self, X, Y, "door1")

    def draw(self):
        windowSurface.blit(self.image, self.rect)
        self.image = pygame.image.load('jeu/' + self.stuffName + ".bmp")


class Jumper(Stuff):

    def __init__(self, X, Y):
        Stuff.__init__(self, X, Y, "jumper")
        self.sound = pygame.mixer.Sound('sons/jumper.wav')


class Coin(Stuff):

    def __init__(self, X, Y):
        Stuff.__init__(self, X, Y, "coin")


class Background(Stuff):

    def __init__(self, X, Y):
        Stuff.__init__(self, X, Y, "bg")


class Spikes(Stuff):

    def __init__(self, X, Y):
        Stuff.__init__(self, X, Y, "spikes")


class Level:

    def __init__(self, levelNumber):

        self.levelName = 'levels/level' + str(levelNumber) + '.txt'
        self.levelList = []
        self.collisionList = []
        self.numberOfCoins = 0

    def readMap(self):

        f = open(self.levelName, 'r')

        g = list(f)

        l = []
        for s in g:
            l += [list(s)]

        for i in range(len(l) - 1):
            l[i].pop()
        return l

    def createLevelPlatformList(self):
        self.levelList = self.readMap()

        for j in range(len(self.levelList)):
            for i in range(len(self.levelList[j])):
                if self.levelList[j][i] == 't':
                    self.collisionList.append((Platform(i, j), 't'))
                elif self.levelList[j][i] == 'd':
                    self.collisionList.append((Door(i, j), 'd'))
                elif self.levelList[j][i] == 'm':
                    self.collisionList.append((Jumper(i, j), 'm'))
                elif self.levelList[j][i] == 'c':
                    self.collisionList.append((Coin(i, j), 'c'))
                    self.numberOfCoins += 1
                elif self.levelList[j][i] == 's':
                    self.collisionList.append((Spikes(i, j), 's'))

    def set_LevelPlatformList(self):
        self.createLevelPlatformList()


currentLevel = 0

char = Character(20, 500)

levelBackground = pygame.image.load('jeu/bg.bmp')
levelBackground.set_colorkey(GREY)
menuBackground = pygame.image.load('menu/bg.bmp')
menuBackground.set_colorkey(GREY)
victoryBackground = pygame.image.load('menu/victory.bmp')
victoryBackground.set_colorkey(GREY)
gameOverBackground = pygame.image.load('menu/gameOver.bmp')
gameOverBackground.set_colorkey(GREY)

inGame = False
inMenu = True
victory = False
gameOver = False

while True:

    if inGame:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_LEFT and char.dx < 0:
                    char.stop()
                if event.key == K_RIGHT and char.dx > 0:
                    char.stop()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    inGame = False
                    inMenu = True
                if event.key == K_LEFT:
                    char.moveLeft()
                if event.key == K_RIGHT:
                    char.moveRight()
                if event.key == K_UP:
                    char.jump(level.collisionList)

        if char.win:
            if currentLevel < 8:
                currentLevel += 1
                level = Level(currentLevel)
                level.set_LevelPlatformList()
                char.rect.bottom = 560
                char.rect.left = 20
                char.allCoins = False
                char.win = False
            else:
                victory = True
                inGame = False
                inMenu = False

        if char.allCoins:
            for c in level.collisionList:
                if c[1] == 'd':
                    c[0].stuffName = 'door2'

        if char.dead:
            pygame.time.wait(100)
            level = Level(currentLevel)
            level.set_LevelPlatformList()
            char.rect.bottom = 560
            char.rect.left = 20
            char.coins = 0
            char.allCoins = False
            char.dead = False

        if char.lives == 0:
            currentLevel = 0
            char = Character(20, 500)
            inGame = False
            inMenu = False
            gameOver = True
            victory = False

        windowSurface.blit(levelBackground, (0, 0))

        for plat in level.collisionList:
            plat[0].draw()

        char.draw()  # dessine le perso
        char.move(level)

    elif inMenu:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    inMenu = False
                    inGame = True
        windowSurface.blit(menuBackground, (0, 0))

    elif victory:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    inMenu = True
                    inGame = False
                    victory = False
                    gameOver = False
                    currentLevel = 0
                    char = Character(20, 500)
        windowSurface.blit(victoryBackground, (0, 0))

    elif gameOver:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    inMenu = True
                    inGame = False
                    victory = False
                    gameOver = False
                    currentLevel = 0
                    char = Character(20, 500)
        windowSurface.blit(gameOverBackground, (0, 0))

        # mets à jour l'écran
    pygame.display.flip()

    # démarrer l'horloge
    mainClock.tick(FPS)
