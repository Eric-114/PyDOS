import pygame,sys
import random
from pygame.locals import *
class Use():
    def Use2(self):
        WIDTH = 480
        HEIGHT = 700
        FPS = 60
        WHITE = (255,255,255)
        BLACK = (0,0,0)
        RED = (255,0,0)
        GREEN = (0,255,0)
        BLUE = (0,0,255)
        pian="me.png"
        opian='enemy1.png'
        danpian='bullet1.png'
        beijing='bg1.png'
        k=0

        #类
        class Plane(pygame.sprite.Sprite):
            def __init__(self,where,speed):
                pygame.sprite.Sprite.__init__(self)
                self.image=[pygame.image.load(f'me{i+1}.png').convert_alpha() for i in range(2)]
                self.rect =self.image[0].get_rect()
                self.rect.topleft = where
                self.speed=speed
            def update(self):
                key = pygame.key.get_pressed()
                if key[pygame.K_RIGHT]:
                    if self.rect.right < WIDTH:
                        self.rect.right += self.speed
                    else:
                        self.rect.right= WIDTH
                if key[pygame.K_LEFT]:
                    if self.rect.left >0:
                        self.rect.left -= self.speed
                    else:
                        self.rect.left= 0
                if key[pygame.K_DOWN]:
                    if self.rect.bottom < HEIGHT:
                        self.rect.bottom += self.speed
                    else:
                        self.rect.bottom= HEIGHT
                if key[pygame.K_UP]:
                    if self.rect.top >0:
                        self.rect.top -= self.speed
                    else:
                        self.rect.top= 0
            def shoot(self):
                dan=Dan(danpian,self.rect.centerx,self.rect.top)
                dans.add(dan)
        class Otherplane(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
        #        self.images=[pygame.image.load(f'mob{i-1}.png').convert_alpha() for d in range(4)]
                self.image = pygame.image.load('mob0.png').convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(0,WIDTH-self.rect.width)
                self.rect.y = random.randrange(-60,-40)
                self.speedx = random.randrange(-2,2)
                self.speedy = random.randrange(1,8)
            def update(self):
                global HEIGHT,WIDTH
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.top >= HEIGHT+10:
                    self.rect.x = random.randrange(0, WIDTH - self.rect.width)
                    self.rect.y = random.randrange(-100, -40)
                    self.speed = random.randrange(1, 8)
        class Dan(pygame.sprite.Sprite):
            def __init__(self,pian,x,y):
                pygame.sprite.Sprite.__init__(self)
                self.image=pygame.image.load(pian).convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.centerx = x
                self.rect.bottom = y
                self.speedy=-10
            def draw(self,screen):
                screen.blit(self.image,self.rect)
            def update(self):
                global HEIGHT,WIDTH
                self.rect.y += self.speedy

        pygame.init()
        #pygame.mixer.init()
        screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Go for it!")
        clock=pygame.time.Clock()
        p=Plane((200,500),5)

        #精灵组
        mobs=pygame.sprite.Group()
        for i in range(1,10):
            mobs.add(Otherplane())
        dans=pygame.sprite.Group()

        #font
        score=0
        font=pygame.font.SysFont("Arial",32)
        text = font.render("Score:0" , True, (255, 255, 255))

        #滚动
        y1=0
        y2=-HEIGHT
        bei1=pygame.image.load(beijing)
        bei2=pygame.image.load(beijing)

        running=True
        while running:
            screen.fill((200,200,200))
            #滚动
            y1+=1
            y2+=1
            if y1>HEIGHT:
                y1=0
            if y2>0:
                y2=-HEIGHT
            screen.blit(bei1,(0,y1))
            screen.blit(bei2, (0, y2))

            clock.tick(FPS)
            p.update()
            screen.blit(p.image[int(k) % 2], p.rect)
            k+=0.1
            #一对多碰撞
            #hits=pygame.sprite.spritecollide(p,mobs,True)
            #if hits:
            #    running=False
            #for i in range(10):
            #    screen.blit(mobs.image[0],mobs.rect())
            #mobs.update()
            #多对多碰撞
            hits1=pygame.sprite.groupcollide(mobs,dans,True,True)
            if hits1:
                mobs.add(Otherplane())
                score+=100
                text = font.render("Score:" + str(score), True, (255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False
                elif event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        p.shoot()
            dans.draw(screen)
            dans.update()
            screen.blit(text,(200,10))
            pygame.display.update()
