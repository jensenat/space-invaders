import pygame
import random
import math

from pygame import mixer


pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

#Title and Icon
icon = pygame.image.load("assets/images/outer-space.png")
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icon)

#Background
background = pygame.image.load("assets/starfield.jpg")

#Player
playerImg = pygame.image.load("assets/images/space-ship.png")
playerX = 370
playerY = 500
playerX_change = 0

def drawPlayer(x, y): 
    screen.blit(playerImg, (x, y))

#Enemy Setup
enemyPortraits = []
for i in range(10):
    enemyImagePath = "assets/images/alien_" + str(i+1) + ".png"
    enemyPortraits.append(pygame.image.load(enemyImagePath))

enemyImg = []
enemyX = []
enemyY = []
enemy_speed = 3
enemyX_change = []
enemyY_change = 66
enemy_numbers = 8

for i in range(enemy_numbers):
    enemyX.append(0 + (80 * i))
    enemyY.append(0)
    enemyX_change.append(enemy_speed)
    enemyImg.append(enemyPortraits[random.randint(0,9)])

def drawEnemy(i, x, y): 
    screen.blit(enemyImg[i], (x, y))

def changeEnemySpeed():
    for i in range(enemy_numbers):
        if enemyX_change[i] < 1:
            enemyX_change[i] = enemy_speed * -1
        else: 
            enemyX_change[i] = enemy_speed

#Bullet Setup
bulletImg = pygame.image.load("assets/images/bullet.png")
bulletSound = mixer.Sound("assets/sounds/laser.wav")
bulletX = 0
bulletY = 500
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

#Game Score
game_score = 0
scoreFont = pygame.font.Font("assets/fonts/Carista.ttf", 32)
scorePosX = 720
scorePosY = 560

def show_score(x, y):
    score = scoreFont.render("Score: " + str(game_score), True, (255, 255, 255))
    screen.blit(score, (x, y))

#Background Music
mixer.music.load("assets/sounds/background.wav")
mixer.music.play(-1)

#Explosion Sound
explosionSound = mixer.Sound("assets/sounds/explosion.wav")

#Game Over
gameOverFont = pygame.font.Font("freesansbold.ttf", 48)
gameOverX = 140
gameOverY = 250

def displayGameOver(x, y):
    gameOver = gameOverFont.render("Game Over - You Suck", True, (255, 0, 0))
    screen.blit(gameOver, (x, y))

#Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bulletSound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    # Add background color
    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))

    #Player position
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    #Check Score to decide whether to increment the speed of the game. 
    if game_score == 5:
        enemy_speed = 4
        changeEnemySpeed()
    elif game_score == 10:
        enemy_speed = 4.5
        changeEnemySpeed()
    elif game_score == 15:
        enemy_speed = 5
        changeEnemySpeed()
    elif game_score == 20:
        enemy_speed = 5.5
        changeEnemySpeed()


    #Enemies Loop
    for i in range(enemy_numbers):
        #Check enemy position to change direction if needed
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX[i] = 0
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change
        elif enemyX[i] > 736:
            enemyX[i] = 736
            enemyX_change[i] = enemy_speed * -1
            enemyY[i] += enemyY_change

        #Bullet-Enemy Collision detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound.play()
            bulletY = 500
            bullet_state = "ready"
            enemyX[i] = 0
            enemyY[i] = 0
            enemyX_change[i] = enemy_speed
            enemyImg[i] = enemyPortraits[random.randint(0,9)]
            game_score += 1

        #GameOver Conditions
        if enemyY[i] > 450 and enemyX[i] <= playerX:
            for j in range(enemy_numbers):
                enemyY[j] = 2000
                playerY = 2000
                displayGameOver(gameOverX, gameOverY)
            break

        #Draw Enemy
        drawEnemy(i, enemyX[i], enemyY[i])

    #Bullet Management
    if bulletY <= -32:
        bulletY = 500
        bullet_state = "ready"

    if (bullet_state == "fire"):
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    #Add a player
    drawPlayer(playerX, playerY)

    #Show Score
    show_score(scorePosX, scorePosY)

    #Update the screen
    pygame.display.update()
    clock.tick(60)