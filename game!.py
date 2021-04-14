#https://blog.naver.com/samsjang/220710524226

import pygame
import random

from time import sleep

white = (255, 255, 255)
p_width = 1024
p_height = 512
background_width = 1024
bat_width = 110

aircraft_width = 90
aircraft_height = 55

bat_width = 90
bat_height = 55

fireball1_width = 140
fireball1_height = 60
fireball2_width = 86
fireball2_height = 60

def textObj(text, font):
    textSurface = font.render(twxt, True, RED)
    return textSurface, textSurface.get_rect()

def dispMassage(text):
    global gamepad

    largeText = pygame.font.Font("freesansbold.ttf", 115)
    TextSurf, TextRect = textObj(text, largeText)
    TextRect.center = ((p_width/2), (p_height/2))
    gamepad.blit(TextSurf, TextRect)
    pygame.display,update()
    sleep(2)
    runGame()

def crash():
    global gamepad
    dispMassage("Crashed!")

def drawObj(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))

def back(background, x, y):
    global gamepad
    gamepad.blit(background, (x, y))

def airplane(x, y):
    global gamepad, aircraft
    gamepad.blit(aircraft, (x, y))

def runGame():
    global gamepad, clock, aircraft, background1, background2
    global bat, fires, bullet, boom

    isShotBat = False
    boom_count = 0

    bullet_xy = []

    x = p_width * 0.05
    y = p_height * 0.8
    y_change = 0

    background1_x = 0
    background2_x = background_width

    bat_x = p_width
    bat_y = random.randrange(0, p_height)

    fire_x = p_width
    fire_y = random.randrange(0, p_height)

    random.shuffle(fires)
    fire = fires[0]
    
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5
                elif event.key == pygame.K_LCTRL:
                    bullet_x = x + aircraft_width
                    bullet_y = y + aircraft_height / 2
                    bullet_xy.append([bullet_x, bullet_y])
                    
                elif event.key == pygame.K_SPACE:
                    sleep(5)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        y += y_change
        
        if y < 0:
            y = 0
        elif y > p_height - aircraft_height:
            y = p_height - aircraft_height
        
        gamepad.fill(white)

        background1_x -= 2
        background2_x -= 2

        bat_x -= 7
        if bat_x <= 0:
            bat_x = p_width
            bat_y = random.randrange(0, p_height)

        if fire == None:
            fire_x -= 30
        else:
            fire_x -= 15

        if fire_x <= 0:
            fire_x = p_width
            fire_y = random.randrange(0, p_height)
            random.shuffle(fires)
            fire = fires[0]
        
        if background1_x == -background_width:
            background1_x = background_width

        if background2_x == -background_width:
            background2_x = background_width
            
        
        back(background1, background1_x, 0)
        back(background2, background2_x, 0)

        drawObj(bat, bat_x, bat_y)
        if fire != None:
            drawObj (fire, fire_x, fire_y)
        drawObj(aircraft, x, y)
        
        airplane(x, y)

        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[0] += 15
                bullet_xy[i][0] = bxy[0]

                if bxy[0] > bat_x:
                    if bxy[1] > bat_y and bxy[1] < bat_y + bat_height:
                        bullet_xy.remove(bxy)
                        isShotBat = True
                
                if bxy[0] >= p_width:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObj(bullet, bx, by)

        if not isShotBat:
            drawObj(bat, bat_x, bat_y)
        else:
            drawObj(boom, bat_x, bat_y)
            boom_count += 1
            if boom_count > 5:
                boom_count = 0
                bat_x = p_width
                bat_y = random.randrange(0, p_height - bat_height)
                isShotBat = False
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

def initGame():
    global gamepad, clock, aircraft, background1, background2
    global bat, fires, bullet, boom

    fires = []

    pygame.init()
    gamepad = pygame.display.set_mode((p_width, p_height))
    pygame.display.set_caption("PyFlying")
    aircraft = pygame.image.load("plane_oo.png")
    background1 = pygame.image.load("background_t.png")
    background2 = background1.copy()
    bat = pygame.image.load("bat.png")
    fires.append(pygame.image.load("fireball.png"))
    fires.append(pygame.image.load("fireball2.png"))
    for i in range(5):
        fires.append(None)
    bullet = pygame.image.load("bullet.png")
    boom = pygame.image.load("boom.png")

    clock = pygame.time.Clock()
    runGame()

    
initGame()
