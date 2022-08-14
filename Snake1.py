import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Slither")
icon = pygame.image.load('snakehead.png')
pygame.display.set_icon(icon)


img = pygame.image.load('snakehead.png')
img = pygame.transform.scale(img,(20,20))
apple = pygame.image.load('apple2.png')
apple = pygame.transform.scale(apple,(30,30))


clock = pygame.time.Clock()
block_size = 20
AppleThickness = 30
FPS = 10
direction = "right"

smallfont = pygame.font.SysFont('comicsansms',25)
medfont = pygame.font.SysFont('comicsansms',50)
largefont = pygame.font.SysFont('comicsansms',80)

def pause():
    paused = True
    message_to_screen("Paused",(0,0,0),-100,size="large")
    message_to_screen("Press C to continue or Q to quit",(0,0,0),25)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused= False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill((0,0,0))
        
        clock.tick(5)
            
def score(score):
    text = smallfont.render("Score: "+str(score),True,(0,0,0))
    gameDisplay.blit(text,[0,0])
def randAppleGen():
    randAppleX = round(random.randrange(0,display_width-AppleThickness))
    randAppleY = round(random.randrange(0,display_height-AppleThickness))
    return randAppleX, randAppleY
randAppleX,randAppleY = randAppleGen()

def gameIntro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill((255,255,255))
        message_to_screen("Welcome to Slither",(0,155,0),-100,"large")
        message_to_screen("The objective of the game is to eat red apples",(0,0,0),-30)
        message_to_screen("The more apples you eat, the longer you get",(0,0,0),10)
        message_to_screen("If you collide with yourself or edges ,you die!",(0,0,0),50)
        message_to_screen("Press C  to play or Q to quit.",(0,0,0),180)
        pygame.display.update()
        clock.tick(15)

def snake(block_size,snakeList):
    if direction == "right":
        head = pygame.transform.rotate(img,90)
    elif direction == "left":
        head = pygame.transform.rotate(img,270)
    elif direction == "up":
        head = pygame.transform.rotate(img,180)
    elif direction == "down":
        head = img
    gameDisplay.blit(head,(snakeList[-1][0] , snakeList[-1][1]))
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay,(0,155,0),[XnY[0],XnY[1],block_size,block_size])

def message_to_screen(msg,color,y_displace=0,size="small"):
    if size == "small":
        screen_text = smallfont.render(msg,True,color)
    elif size == "medium":
        screen_text = medfont.render(msg,True,color)
    elif size == "large":
        screen_text = largefont.render(msg,True,color)
    
    text_rect = screen_text.get_rect(center = [display_width/2 ,display_height/2+y_displace])
    gameDisplay.blit(screen_text,text_rect)

def gameLoop():
    global direction
    direction = "right"
    gameExit = False
    gameOver = False
    
    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = 10
    lead_y_change = 0
    snakeList = []
    snakeLength = 1

    randAppleX,randAppleY = randAppleGen()

    while not gameExit:
        if gameOver == True:
            message_to_screen("Game over",(255,0,0),-50,size = 'large')
            message_to_screen("Press C to play again or Q to quit",(0,0,0),50,size="medium")
            pygame.display.update()

        while gameOver == True:
            gameDisplay.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.event.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                          gameExit = True
                          gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = - block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                
                elif event.key == pygame.K_p:
                    pause()

        if lead_x >=display_width or lead_x <0 or lead_y >=display_height or lead_y < 0 :
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill((255,255,255))

     
        #pygame.draw.rect(gameDisplay,(255,0,0),[randAppleX,randAppleY,AppleThickness,AppleThickness])
        gameDisplay.blit(apple,(randAppleX,randAppleY))
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]
        
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
        
        snake(block_size,snakeList)

        score(snakeLength-1)
        pygame.display.update()

        if lead_x >  randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size<randAppleX+ AppleThickness:
            if lead_y >= randAppleY and lead_y <= randAppleY + AppleThickness:
                randAppleX,randAppleY = randAppleGen()
                snakeLength+=1
        
            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                randAppleX,randAppleY = randAppleGen()
                snakeLength+=1
        clock.tick(FPS)

    pygame.quit()
    quit()

gameIntro()
gameLoop()