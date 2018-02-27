import pygame, sys, shelve, pickle
import time as Time
from decimal import Decimal
pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (10, 200, 40)   
RED = pygame.Color('red')
DISPLAYSURF = pygame.display.set_mode((460, 720))
clock = pygame.time.Clock()
logo = pygame.image.load('pngImages/Logo.png')
menu = pygame.image.load('pngImages/menu.png')
storeBoard = pygame.image.load('pngImages/storeBoard.png')
loadingBar = pygame.image.load('pngImages/loadingBar.png')
mainMenu = pygame.image.load('pngImages/mainMenu.png')
background = pygame.image.load('pngImages/background.png')
Font1 = pygame.font.SysFont('monaco', 24)
Font2 = pygame.font.SysFont('monaco', 30)
cash = 5
barlength = 102 # the lenght of the growing bar 

def buyDraw(amount, minxbuy, minybuy):
    buySurface = Font1.render('{0}'.format(amount), True, BLACK)
    buyRect = buySurface.get_rect()
    buyRect.midtop = (85, minybuy)
    DISPLAYSURF.blit(buySurface, buyRect)
def cashDraw(cash):
    cashSurface = Font2.render(' ${0}'.format(cash), True, GREEN)
    cashRect = cashSurface.get_rect()
    cashRect.midtop = (387, 10)
    DISPLAYSURF.blit(cashSurface, cashRect)

def capitalistOne(amount, cost, timez, gain, minxbuy, maxxbuy, minybuy, maxybuy, minxgain, maxxgain, minygain, maxygain, cash):
    pygame.display.set_caption('capitalist')
    buy_button = pygame.Rect(minxbuy, minybuy, maxxbuy, maxybuy)
    gain_button = pygame.Rect(minxgain, minygain, maxxgain, maxygain)
    menuRect = pygame.Rect(400, 680, 30, 30)
    coefficient = maxxgain / timez # 
    time = 0
    dt = 0
    upgrade = amount * gain
    loop = False

    while True:    
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()   
        inc = time * coefficient
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f = open('store.pckl', 'wb')
                pickle.dump(amount, f)
                f.close()
                pygame.quit()
                sys.exit()
            
                #Return to menu
            if menuRect.collidepoint(mouse_pos) and mouse_pressed[0]:
                f = open('store.pckl', 'wb')
                pickle.dump(amount, f)
                f.close()
                opening()

                # Max LVL
            if buy_button.collidepoint(mouse_pos) and mouse_pressed[0] and amount >= 1000:
                maxLvlSurface = Font1.render('Max Lvl Reached', True, RED)
                maxLvlRect = maxLvlSurface.get_rect()
                maxLvlRect.midtop = (215, 5)
                DISPLAYSURF.blit(maxLvlSurface, maxLvlRect)
                pygame.display.flip()
                Time.sleep(0.5)
          
            # buy button
            if buy_button.collidepoint(mouse_pos) and mouse_pressed[0] and cash >= cost and amount < 1000:
                amount += 1
                cash -= cost
                upgrade = amount * gain
          
                #Gain Button
        if gain_button.collidepoint(mouse_pos) and mouse_pressed[0] and amount > 0:
            loop = True # alows the user to click, then have the bar grow, rather than while they are clicking run it
        if loop == True:
            if time < timez: # if the bar isnt full, add to it
                time += dt
        if time >= timez: # if the bar is full, reset time, give cash.
            cash += upgrade
            time = 0
            loop = False
       
        # Draw everything 
        DISPLAYSURF.blit(background, (0,0))
        DISPLAYSURF.blit(storeBoard, (0,0)) # Draw the icons, ect.
        pygame.draw.rect(DISPLAYSURF, GREEN, (minxgain + 1, minygain, inc, maxygain)) # Draws a portion of the green bar
        pygame.draw.rect(DISPLAYSURF, BLACK, gain_button, 2) # draws a border around the gain bar
        DISPLAYSURF.blit(mainMenu, (400, 680))# draws a main menu button to return to main menu 
        buyDraw(amount, minxbuy, minybuy)# draws the buy button

            # Should the cash be displayed in Sci Notation or in standar
        if int(cash) < 1000000:
            cashDraw(cash)
        if int(cash) > 1000000:
            SciNot = '%.2E' % Decimal(str(cash))
            cashDraw(SciNot)
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000 

def opening():
    DISPLAYSURF.blit(background, (0,0))
    DISPLAYSURF.blit(logo, (155, 50))
    DISPLAYSURF.blit(menu, (0 , 125))
    saveRect = pygame.Rect(400, 680, 30, 30)
    pygame.display.set_icon(logo)
    pygame.display.flip()
    f = open('store.pckl', 'rb')
    gShovelAmount = pickle.load(f)
    f.close()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                if x < 375 and x > 80 and y < 545 and y > 395:
                    capitalistOne(
                        amount=gShovelAmount, cost=5, timez=10, gain=5, minxbuy=21,
                        maxxbuy=41, minybuy=21, maxybuy=41, minxgain=120,
                        maxxgain=204, minygain=21, maxygain=41, cash=cash) 
opening()
