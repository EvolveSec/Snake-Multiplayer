import pygame
from pygame.locals import *
import sys
import random
import time
import math

pygame.init()

#create surface object
width, height = 1000, 960
monitorInfo = pygame.display.Info()
screen=pygame.display.set_mode((width, height))
#create time object (keeps track of FPS)
clock = pygame.time.Clock()
#colours
GREEN = (0,255,0)
BLACK = (0,0,0)
CYAN = (175,238,238)
YELLOW = (255,255,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GOLD = (255,255,153)
PURPLE = (147,112,219)
GREEN = (0,255,0)
            
class foodClass(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #sets color and initial position of food
        self.image = pygame.Surface((20,20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.newPos()

    def newPos(self):
        #sets new position of food 
        self.possiblePosX = range(20, width, 20)
        self.possiblePosY = range(20, height, 20)
        self.rect.x = random.choice(self.possiblePosX)
        self.rect.y = random.choice(self.possiblePosY)

    def update(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
class blockClass(pygame.sprite.Sprite):
    
    def __init__(self, x, y, size, color):
        pygame.sprite.Sprite.__init__(self)
        #sets position, color, and size of block
        self.image = pygame.Surface((size,size))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        #draws blocks to surface
        surface.blit(self.image, (self.rect.x, self.rect.y))

class snakeClass(pygame.sprite.Sprite):
    
    def __init__(self, color, demo):
        pygame.sprite.Sprite.__init__(self)
        #creates snake object variables
        self.direction = 270
        self.body = []
        self.color = color
        self.dead = False
        self.score = 0
        self.demo = demo
        self.portals = []
        #creates initial snake body 
        count = 0
        for i in range(15):
            self.body.append(blockClass(60 + count, 60, 20, self.color))
            count += 20

    def checkCollision(self):
        #checks if collision with wall
        if self.body[-1].rect.x > width:
            self.body[-1].rect.x = 0
        elif self.body[-1].rect.x < 0:
            self.body[-1].rect.x = width
        elif self.body[-1].rect.y > height:
            self.body[-1].rect.y = 0
        elif self.body[-1].rect.y < 0:
            self.body[-1].rect.y = height
                    
        #checks if collision with food
        if self.body[-1].rect.colliderect(food.rect):
            food.newPos()
            self.score += 10
            if self.demo:
                del self.body[0]
        else:
            del self.body[0]
            
        #checks if collision with own body
        for i in range(len(self.body[:-1])):
            if self.body[-1].rect.colliderect(self.body[i]):
                self.dead = True
        
    def intelligence(self):
        #intelligence method, moves to food depending on current direction
        if food.rect.y > self.body[-1].rect.y and self.direction != 0:
            self.direction = 180
        elif food.rect.y < self.body[-1].rect.y and self.direction != 180:
            self.direction = 0
        elif food.rect.x < self.body[-1].rect.x and self.direction != 270:
            self.direction = 90
        elif food.rect.x > self.body[-1].rect.x and self.direction != 90:
            self.direction = 270

    def resetValues(self):
        #reset values of snake
        pygame.sprite.Sprite.__init__(self)
        self.direction = 270
        self.body = []
        self.dead = False
        self.score = 0
        self.portals = []

        count = 0
        for i in range(15):
            self.body.append(blockClass(60 + count, 60, 20, self.color))
            count += 20
            
    def update(self, surface):
        #get coordinates of front position of snake
        x_frontPos = self.body[-1].rect.x
        y_frontPos = self.body[-1].rect.y
        #if not a demo snake, activate controls
        if not self.demo:
            #returned pressed keys
            key = pygame.key.get_pressed()
            #change direction of snake depending on key press
            if key[pygame.K_s]: 
                if self.direction != 0:
                    self.direction = 180
            elif key[pygame.K_w]:
                if self.direction != 180:
                    self.direction = 0
            elif key[pygame.K_a]:
                if self.direction != 270:
                    self.direction = 90
            elif key[pygame.K_d]:
                if self.direction != 90:
                    self.direction = 270
        #update snake depending on direction
        if self.direction == 180: 
            self.body.append(blockClass(x_frontPos, y_frontPos + 20, 20, self.color))
        elif self.direction == 0: 
            self.body.append(blockClass(x_frontPos, y_frontPos - 20, 20, self.color))
        elif self.direction == 90: 
            self.body.append(blockClass(x_frontPos - 20, y_frontPos, 20, self.color))
        elif self.direction == 270:
            self.body.append(blockClass(x_frontPos + 20, y_frontPos, 20, self.color))
        #check snake collisions
        self.checkCollision()
        #update snake on screen
        for i in range(len(self.body)):
            self.body[i].image.set_alpha(i*10)
            self.body[i].draw(surface)
        #update portals on screen
        for portal in self.portals:
            portal.update(surface)
        #if demo snake, activate A.I
        if self.demo:
            self.intelligence()
        
#load background images
background = pygame.image.load("background.png").convert()
background1 = pygame.image.load("background1.png").convert()
#set game state
gameState = 0
#create snake objects            
snake = snakeClass(CYAN, False)
demoSnake = snakeClass(WHITE, True)
#create food object
food = foodClass()
#create colour selection objects
redButton = blockClass(40, 40, 60, RED)
blueButton = blockClass(40, 100, 60, BLUE)
greenButton = blockClass(40, 160, 60, GREEN)
#create font
basicFont = Font = pygame.font.Font("Squared Display.ttf", 30)
#load and start music
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
endSound = pygame.mixer.Sound("game_over.wav")
pygame.mixer.music.play(-1)
    
active = True
            
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #get keys pressed
    key = pygame.key.get_pressed()

    #if in first state (menu state)
    if gameState == 0: 
        #update background and logo image
        screen.fill(BLACK)
        screen.blit(background1, (0,0))
        #update demo snake
        demoSnake.update(screen)
        #if enter button clicked, change game state
        if key[pygame.K_RETURN]:
                gameState = 1

    #if in second state (gameplay state)
    if gameState == 1:
        #update background
        screen.fill(BLACK)
        screen.blit(background, (0,0))
        #update snake and food
        snake.update(screen)
        food.update(screen)
        #update text
        text = basicFont.render('Player 1 score:' + str(snake.score), True, WHITE)
        screen.blit(text, (5,5))

        if snake.dead: #if snake dies, reset
            endSound.play()
            time.sleep(1)
            demoSnake.resetValues()
            snake.resetValues()
            gameState = 0
            
    pygame.display.update()
    clock.tick(30)
