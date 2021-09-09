# -*- coding: utf-8 -*-
"""
Created on Sat May 25 13:11:50 2019

@author: МЫ
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 11:36:03 2019

@author: МЫ
"""
import random
import math
import sys
import pygame
LENGTH = 1400
WIDTH = 700
center=(LENGTH/2,WIDTH/2)
    
FPS=40
sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
def gr(x,y,x0,y0,G,M):
    r = ((x-x0)**2 + (y-y0)**2)**0.5
    g_x=-(G*M/r**2)*(x-x0)/r
    g_y=-(G*M/r**2)*(y-y0)/r
    return (g_x, g_y)

class Star(pygame.sprite.Sprite):
    def __init__(self):
        self.surf = pygame.Surface((100,100))
        self.surf.fill((8,23,43))
        self.rect =self.surf.get_rect(center=(LENGTH/2,WIDTH/2))
        pygame.draw.circle(self.surf,(243,165,5),(50,50),50)
        self.Mass=15000
        
    def gravity(self,x,y):
        G= 0.00021
        return gr(x, y, self.rect.x, self.rect.y, G, self.Mass)
def gameOver(player):
                player.surf =pygame.Surface((1,1))
                player.surf.fill((8,23,43))
                player.original_surf=player.surf;
                player.gameover = True
class Player(pygame.sprite.Sprite):
    
    def __init__(self,number):       
        super().__init__()
        if number == 1:
            self.surf = pygame.image.load('ship.gif')
            self.eminem = pygame.image.load('ship_thrust.gif')
        else:
            self.surf = pygame.image.load('ship_2.gif')
            self.eminem = pygame.image.load('ship_2_thrust.gif')
        self.engine_vel=1
        self.engine=0
        self.surf.set_colorkey((255,255,255))
        self.eminem.set_colorkey((255,255,255))
        if number == 1:
            self.rect = self.surf.get_rect(center=(100, WIDTH/2 - 100))
        else:
            self.rect = self.surf.get_rect(center=(1100, WIDTH/2 - 100))
        
        self.original_surf=self.surf;
        self.vel_x=0
        self.vel_y=0
        if number == 1 :
            self.angle=0
        else:
            self.angle=180
        self.gameover=False
        self.number = number
    
     
    def povorot(self,key,thrusted):
        if self.number == 1:
            ship1=self.original_surf;
            ship=self.rect
            if key == 'a':    
                self.angle=self.angle+5
            elif key == 'd':
                self.angle=self.angle-5
            elif key == 'w':
                self.angle=self.angle
            angle=self.angle
            if not thrusted:
                ship1=self.original_surf;
                ship2=pygame.transform.rotate(ship1,angle)
            else:
                ship1=self.eminem
                ship2=pygame.transform.rotate(ship1,angle)
            return (ship2,ship) 
            
        else:
            ship1=self.original_surf;
            ship=self.rect
            if key == 'K_LEFT':    
                self.angle=self.angle+5
            elif key == 'K_RIGHT':
                self.angle=self.angle-5
            elif key == 'K_UP':
                self.angle=self.angle
            angle=self.angle
            if not thrusted:
                ship1=self.original_surf;
                ship2=pygame.transform.rotate(ship1,angle)
            else:
                ship1=self.eminem
                ship2=pygame.transform.rotate(ship1,angle)
            return (ship2,ship) 
    def update(self,SUN):
        if self.number == 2:
            pressed_key = pygame.key.get_pressed()
            if pressed_key[pygame.K_UP]:
                self.engine=1
                (self.surf,self.rect) =self.povorot('K_UP',True)
            else:
                self.engine=0
                (self.surf,self.rect)=self.povorot('K_UP',False)
            if pressed_key[pygame.K_LEFT]:
                if self.engine==0:
                    (self.surf,self.rect)=self.povorot('K_LEFT',False)
                else:
                    (self.surf, self.rect)=self.povorot('K_LEFT',True)
            if pressed_key[pygame.K_RSHIFT]:
                pulka=Pulka(self.rect,self.angle,1)
                bullets.add(pulka)
            if pressed_key[pygame.K_RIGHT]:
                if self.engine==0:
                    (self.surf,self.rect)=self.povorot('K_RIGHT',False)
                else:
                    (self.surf,self.rect)=self.povorot('K_RIGHT',True)
                    
        else:
            pressed_key = pygame.key.get_pressed()
            if pressed_key[pygame.K_w]:
                self.engine=1
                (self.surf,self.rect) =self.povorot('w',True)
            else:
                self.engine=0
                (self.surf,self.rect)=self.povorot('w',False)
            if pressed_key[pygame.K_a]:
                if self.engine==0:
                    (self.surf,self.rect)=self.povorot('a',False)
                else:
                    (self.surf, self.rect)=self.povorot('a',True)
            if pressed_key[pygame.K_SPACE]:
                pulka=Pulka(self.rect,self.angle,1)
                bullets.add(pulka)
            if pressed_key[pygame.K_d]:
                if self.engine==0:
                    (self.surf,self.rect)=self.povorot('d',False)
                else:
                    (self.surf,self.rect)=self.povorot('d',True)
        (gx_save,gy_save)=SUN.gravity(self.rect.x,self.rect.y)
        x_save = self.rect.x+self.vel_x
        y_save = self.rect.y + self.vel_y
        gx = 0.5*(gx_save + SUN.gravity(x_save,y_save)[0])
        gy = 0.5*(gy_save + SUN.gravity(x_save, y_save)[1])
        
        
        self.rect.x += self.vel_x + gx*0.5
        self.rect.y += self.vel_y + gy*0.5
        self.vel_x += gx +self.engine*self.engine_vel*math.cos((self.angle)*math.pi/180)
        self.vel_y += gy -self.engine*self.engine_vel*math.sin((self.angle)*math.pi/180)
        if self.rect.left > LENGTH: self.rect.right=0
        if self.rect.right<0: self.rect.left=LENGTH
        if self.rect.top>WIDTH:self.rect.bottom=0
        if self.rect.bottom<0:self.rect.top=WIDTH    
    
            
        
        

class Pulka(pygame.sprite.Sprite):
    def __init__(self,position,angle,number):
        super().__init__()
        
        self.pulkao = pygame.Surface((4,4))
        self.pulkao.fill((255,36,2))
        self.angle=angle
        newposition =(int(position[0]+13),int(position[1]+10)) ##-10*math.sin(angle*math.pi/180)+10*math.cos(angle*math.pi/180)"""
        self.rect = self.pulkao.get_rect(center=newposition)
        self.velocityX=50*math.cos(angle*math.pi/180)
        self.velocityY=50*math.sin(angle*math.pi/180)
    def update(self):
        self.rect.x+= self.velocityX
        self.rect.y-= self.velocityY
        
    
        

class Game:
    def main(self,screen):
        clock = pygame.time.Clock()
        background = pygame.Surface(screen.get_size())
        background.fill((8,23,43))
                
        SUN=Star()
        player = Player(1)
        player2 = Player(2)
  
        sprites.add(player,player2)       
        while True:
            dt = clock.tick(FPS)
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit() 
                    if event.key == pygame.K_r:
                        
                        pygame.init()
                        screen = pygame.display.set_mode((LENGTH, WIDTH))
                        pygame.display.set_caption('Space Y')
                        game=Game()
                        game.main(screen)

            
            screen.blit(background, (0,0))
            screen.blit(SUN.surf,SUN.rect)
            if  (player.gameover == False) and (player2.gameover == False):
                player.update(SUN)
                player2.update(SUN)
            screen.blit(player.surf,player.rect)
            screen.blit(player2.surf,player2.rect)
            for bullet in bullets:
                bullet.update()
                screen.blit(bullet.pulkao,bullet.rect)
                        
            collision=pygame.sprite.collide_circle_ratio(0.8)
            if collision(player,SUN) or pygame.sprite.spritecollide(player,bullets,dokill=True, collided = collision):
                gameOver(player)
            if collision(player2,SUN) or pygame.sprite.spritecollide(player2,bullets,dokill=True, collided = collision):
                gameOver(player2)
                
            if collision(player,player2):
                gameOver(player)
                gameOver(player2)
            if player.gameover and not player2.gameover:
                font = pygame.font.Font(None, 50)
                text = font.render('player2 WINS ',True,(255,255,0))
                text_length, text_width = text.get_size()
                screen.blit(text,(LENGTH/2 - text_length/2 + 1 , WIDTH/2- text_width/2 + 100))
            if player2.gameover and not player.gameover:
                font = pygame.font.Font(None, 50)
                text = font.render('player1 WINS ',True,(255,255,0))
                text_length, text_width = text.get_size()
                screen.blit(text,(LENGTH/2 - text_length/2 + 1 , WIDTH/2- text_width/2 + 100))
           
            if player.gameover and (player2.gameover):
                font = pygame.font.Font(None, 50)
                text = font.render('FRIENDSHIP WINS ',True,(255,255,0))
                text_length, text_width = text.get_size()
                screen.blit(text,(LENGTH/2 - text_length/2 + 1 , WIDTH/2- text_width/2 + 100))
            pygame.display.flip()

                

pygame.init()
screen = pygame.display.set_mode((LENGTH, WIDTH))
pygame.display.set_caption('Space Y')
game=Game()
game.main(screen)


    
    
        
    

  