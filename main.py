from pygame import *
import pygame
import random
import sys


width = 600
height = 600
FPS = 40
minsizeE = 10
maxsizeE = 30
minspeedE = 1
maxspeedE = 8
addEnemy = 6
playerMove = 5


def terminate():
    pygame.quit()
    sys.exit()


def pressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


def hitEnemy(playerRect, enemies):
    for b in enemies:
        if playerRect.colliderect(b['rect']):
            return True
    return False


def text(text, font, surface, x, y):
    textobj = font.render(text, 1, (255, 255, 0))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Игра')
pygame.mouse.set_visible(False)

font = pygame.font.SysFont('arial', 30)

gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('bgsound.mp3')

playerImage = pygame.image.load('hero2.png')
playerRect = playerImage.get_rect()
enemy = pygame.image.load('enemy2.png')
bg = pygame.image.load("bg.png")

windowSurface.blit(bg, (0, 0))

text('Нажми на клавишу, чтобы начать', font, windowSurface, (width / 3) - 100, (height / 3) + 50)
pygame.display.update()
pressKey()
with open('score.txt', 'r') as sc:
    topScore = int(sc.read())

while True:
    enemies = []
    score = 0
    playerRect.topleft = (width / 2, height - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    enemyAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True:
        score += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        if not slowCheat:
            enemyAddCounter += 1
        if enemyAddCounter == addEnemy:
            enemyAddCounter = 0
            enemySize = random.randint(minsizeE, maxsizeE)
            newEnemy = {'rect': pygame.Rect(random.randint(0, width - enemySize), 0 - enemySize, enemySize, enemySize),
                        'speed': random.randint(minspeedE, maxspeedE),
                        'surface': pygame.transform.scale(enemy, (enemySize, enemySize)),
                        }

            enemies.append(newEnemy)

        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * playerMove, 0)
        if moveRight and playerRect.right < width:
            playerRect.move_ip(playerMove, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * playerMove)
        if moveDown and playerRect.bottom < height:
            playerRect.move_ip(0, playerMove)

        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        for b in enemies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        for b in enemies[:]:
            if b['rect'].top > height:
                enemies.remove(b)

        bg = pygame.image.load("bg1.png")

        windowSurface.blit(bg, (0, 0))

        text(f'Результат: {score}', font, windowSurface, 10, 0)
        text(f'Лучший результат: {topScore}', font, windowSurface, 10, 40)

        windowSurface.blit(playerImage, playerRect)

        for b in enemies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        if hitEnemy(playerRect, enemies):
            if score > topScore:
                topScore = score
                with open('score.txt', 'r+') as sc:
                    sc.writelines(str(score))
            break

        mainClock.tick(FPS)

    pygame.mixer.music.stop()
    gameOverSound.play()
    bg = pygame.image.load("bg.png")

    windowSurface.blit(bg, (0, 0))
    text(f'Результат: {score}', font, windowSurface, 10, 0)
    text(f'Лучший результат: {topScore}', font, windowSurface, 10, 40)
    text('ИГРА ЗАКОНЧИЛАСЬ', font, windowSurface, (width / 3) - 40, (height / 3))
    text('Нажми на клавишу,', font, windowSurface, (width / 3) - 30, (height / 3) + 50)
    text('чтобы начать заново', font, windowSurface, (width / 3) - 40, (height / 3) + 100)
    pygame.display.update()
    pressKey()
    gameOverSound.stop()
