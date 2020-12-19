import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
screen_x = 800
screen_y = 600
spaceship_len = 64
ufo_len = 64
spaceshipImg = pygame.image.load('Images/spaceship.png')
bulletImg = pygame.image.load('Images/bullet.png')
background = pygame.image.load('Images/background.jpg')
score_value = 0
ufoX = []
ufoY = []
ufo_changeX = []
ufo_changeY = []
ufoImg = []
num_of_ufos = 6
stage = 1
old_ufo_changeX_times_2 = 0.3
old_bulletY_change = 0.7
for i in range(num_of_ufos):
    ufoX.append(random.randint(0, 736))
    ufoY.append(random.randint(0, 60))
    ufo_changeX.append(0.3)
    ufo_changeY.append(60)
    ufoImg.append(pygame.image.load('Images/ufo.png'))
game_display = pygame.display.set_mode((screen_x, screen_y))
spaceshipX = 370
spaceshipY = 480
spaceship_changeY = 0
spaceship_changeX = 0
bulletX = 0
bulletY = spaceshipY
bulletX_change = 0
bulletY_change = 0.7
bullet_ready_or_not = "ready"
font_for_score_and_stage = pygame.font.Font('freesansbold.ttf', 32)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
new_game_font = pygame.font.Font('freesansbold.ttf', 50)

buttonX_new_game = 0
buttonY_new_game = screen_y - 100
fontX_score = 10
fontY_score = 10
fontX_stage = 650
fontY_stage = 0
text_for_new_game = font_for_score_and_stage.render('New Game', True, (255, 0, 0))
distance_for_game_over = math.sqrt((math.pow(ufoX[i] - spaceshipX, 2)) + (math.pow(ufoY[i] - spaceshipY, 2)))


def show_font_game_over(x, y):
    game_over_text_msg = new_game_font.render("Press Any key For New Game", True, (255, 0, 0))
    screen.blit(game_over_text_msg, (x, y))


def show_font_stage(x, y):
    stage_text = font_for_score_and_stage.render("stage: " + str(stage), True, (255, 0, 0))
    screen.blit(stage_text, (x, y))


def show_font_score(x, y):
    score = font_for_score_and_stage.render("score: " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


def collision(bullet_x, bullet_y, ufo_x, ufo_y):
    distance = math.sqrt((math.pow(ufo_x - bullet_x, 2)) + (math.pow(ufo_y - bullet_y, 2)))
    if distance < 27:
        return True


def spaceship(x, y):
    screen.blit(spaceshipImg, (x, y))


def ufo(x, y, k):
    screen.blit(ufoImg[k], (x, y))


def fire_bullet(x, y):
    global bullet_ready_or_not
    bullet_ready_or_not = "fire"
    screen.blit(bulletImg, (x, y + 10))


def game_over_text():
    over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))


def collision_for_game_over(ufoX, ufoY, spaceshipX, spaceshipY):
    distance_for_game_over = math.sqrt((math.pow(ufoX - spaceshipX, 2)) + (math.pow(ufoY - spaceshipY, 2)))
    if distance_for_game_over < 27:
        return True


set_running = True
running = True
last_keydown = ''
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                # checks that the last key down was left so he wont do two key ups at the same time
                if last_keydown == 'left':
                    spaceship_changeX = 0
                    spaceship_changeY = 0
            if event.key == pygame.K_RIGHT:
                # checks that the last key down was right so he wont do two key ups at the same time
                if last_keydown == 'right':
                    spaceship_changeX = 0
                    spaceship_changeY = 0
            if event.key == pygame.K_DOWN:
                # checks that the last key down was down so he wont do two key ups at the same time
                if last_keydown == 'down':
                    spaceship_changeX = 0
                    spaceship_changeY = 0
            if event.key == pygame.K_UP:
                # checks that the last key down was up so he wont do two key ups at the same time
                if last_keydown == 'up':
                    spaceship_changeX = 0
                    spaceship_changeY = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                last_keydown = 'left'
                spaceship_changeX = -0.5
            if event.key == pygame.K_RIGHT:
                last_keydown = 'right'
                spaceship_changeX = 0.5
            if event.key == pygame.K_DOWN:
                last_keydown = 'down'
                spaceship_changeY = 0.5
            if event.key == pygame.K_UP:
                last_keydown = 'up'
                spaceship_changeY = -0.5
            if event.key == pygame.K_SPACE:
                if bullet_ready_or_not == "ready":
                    bulletX = spaceshipX
                    bulletY = spaceshipY
                    fire_bullet(bulletX, bulletY)
    for i in range(num_of_ufos):
        if ufoY[i] >= 470:
            for j in range(num_of_ufos):
                ufoY[j] = 2000
            game_over_text()
            set_running = False

        if collision_for_game_over(ufoX[i], ufoY[i], spaceshipX, spaceshipY):
            for j in range(num_of_ufos):
                ufoY[j] = 2000
            game_over_text()
            set_running = False

        if ufoX[i] <= 0:
            ufoY[i] += ufo_changeY[i]
            ufo_changeX[i] = 0.2
        if ufoX[i] >= screen_x - ufo_len:
            ufoY[i] += ufo_changeY[i]
            ufo_changeX[i] = -0.2
        if collision(bulletX, bulletY, ufoX[i], ufoY[i]):
            if bullet_ready_or_not == "fire":
                bulletY = spaceshipY
                bullet_ready_or_not = "ready"
                score_value += 1
                ufoY[i] = -20000
                if num_of_ufos == score_value:
                    num_of_ufos += 4
                    ufoX = []
                    ufoY = []
                    ufo_changeX = []
                    ufo_changeY = []
                    ufoImg = []
                    ufo_changeX_times_2 = old_ufo_changeX_times_2 * 1.2
                    old_ufo_changeX_times_2 = ufo_changeX_times_2
                    score_value = 0
                    stage += 1
                    for _ in range(num_of_ufos):
                        ufoX.append(random.randint(0, 736))
                        ufoY.append(random.randint(0, 60))
                        ufo_changeX.append(ufo_changeX_times_2)
                        ufo_changeY.append(60)
                        ufoImg.append(pygame.image.load('Images/ufo.png'))

                    spaceshipX = 370
                    spaceshipY = 480
                    spaceship_changeY = 0
                    spaceship_changeX = 0
                    bulletX = 0
                    bulletY = spaceshipY
                    bulletX_change = 0
                    bulletY_change = old_bulletY_change * 1.2
                    old_bulletY_change = bulletY_change
                    bullet_ready_or_not = "ready"

        ufoX[i] += ufo_changeX[i]
        ufo(ufoX[i], ufoY[i], i)
    spaceshipX += spaceship_changeX
    spaceshipY += spaceship_changeY
    if spaceshipX >= screen_x - spaceship_len:
        spaceshipX = screen_x - spaceship_len
    if spaceshipX <= 0:
        spaceshipX = 0
    if spaceshipY <= 0:
        spaceshipY = 0
    if spaceshipY >= screen_y - spaceship_len:
        spaceshipY = screen_y - spaceship_len
    if bullet_ready_or_not == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = spaceshipY
        bullet_ready_or_not = "ready"
    spaceship(spaceshipX, spaceshipY)
    show_font_score(fontX_score, fontY_score)
    show_font_stage(fontX_stage, fontY_stage)
    pygame.display.update()
    while not set_running:
        pos = pygame.mouse.get_pos()
        spaceship(spaceshipX, spaceshipY)
        show_font_score(fontX_score, fontY_score)
        show_font_stage(fontX_stage, fontY_stage)
        show_font_game_over(buttonX_new_game, buttonY_new_game)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                set_running = True
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed():
                    num_of_ufos = 6
                    ufoX = []
                    ufoY = []
                    ufo_changeX = []
                    ufo_changeY = []
                    ufoImg = []
                    score_value = 0
                    stage = 1
                    for _ in range(num_of_ufos):
                        ufoX.append(random.randint(0, 736))
                        ufoY.append(random.randint(0, 60))
                        ufo_changeX.append(0.3)
                        ufo_changeY.append(60)
                        ufoImg.append(pygame.image.load('Images/ufo.png'))

                    spaceshipX = 370
                    spaceshipY = 480
                    spaceship_changeY = 0
                    spaceship_changeX = 0
                    bulletX = 0
                    bulletY = spaceshipY
                    bulletX_change = 0
                    bulletY_change = 0.7
                    bullet_ready_or_not = "ready"
                    set_running = True