import pygame # load pygame keywords
import sys # let python use file system
import os # help python identify your OS
import time
import random
import csv
'''
Variables
'''
ALPHA=(0, 0, 0)
WALPHA=(254,254,254)
BLUE  = (25, 25, 200)
RED = (255, 0, 0)
BLACK = (23, 23, 23)
PURPLE = (150, 0, 150)
WHITE = (254, 254, 254)
GREEN = (0,128,0,1)
BROWN = (165, 42, 42, 1)
GREEN_BROWN = (165,128,42,1)
ORANGE= (156,45,0,4)
LIGHT_GREEN = (42, 159,0,45)

#screenx=1850
#screeny=950
screeny=750
screenx= 1400
worldx=screenx*2
worldy=screeny*2
backwardx=100
forwardx=screenx-backwardx
backwardy=backwardx
forwardy=screeny-backwardy
tx=64
ty=64
steps=10
fps   = 60 # frame rate
ani   = 4   # animation cycles

'''
Objects
'''
class Background():
    
    def __init__(self,x,y,imgfile):
        self.img=pygame.image.load(os.path.join('images',imgfile))
        self.img = pygame.transform.scale(self.img,(worldx, worldy))
        self.x=x
        self.y=y


class Player (pygame.sprite.Sprite):
    max_wood=30
    def __init__ (self, x, y, imgfile="Elf1.png"):
        (sizex, sizey)=(45,45)
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('images',imgfile)).convert()
        img = pygame.transform.scale(img,(sizex, sizey))
      # img.convert_alpha()     # optimise alpha
        #img.set_colorkey(ALPHA) # set alpha
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.sizey=sizey
        self.sizex=sizex
        self.movex=0
        self.movey=0
        self.score=0
        self.wood_carried=0
      
        
    def control(self,x,y):
        self.movex += x
        self.movey += y
        
    def update(self,bg,rlist):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        if self.rect.x -bg.x< backwardx:
#            self.rect.x-=self.movex
            self.rect.x=screenx-backwardx+bg.x
            bg.x=-(worldx-screenx)
            for r in rlist:
                r.rect.x=r.x-(worldx-screenx)
        if self.rect.x-bg.x>worldx-backwardx:
#            self.rect.x-=self.movex
            self.rect.x=backwardx
            bg.x=0
            for r in rlist:
                r.rect.x=r.x
    
        if self.rect.y-bg.y>worldy-backwardy:
            #self.rect.y-=self.movey
            self.rect.y=backwardy
            bg.y=0
            for r in rlist:
                r.rect.y=r.y
        if self.rect.y-bg.y<backwardy:
            #self.rect.y-=self.movey
            self.rect.y=screeny-backwardy+bg.y
            bg.y=-(worldy-screeny)
            for r in rlist:
                r.rect.y=r.y-(worldy-screeny)
        collidelist=pygame.sprite.spritecollide(self,rlist,False)
        for r in collidelist:
            if r.rtype=="wood":
                if self.wood_carried<Player.max_wood:
                    self.wood_carried+=6
                    r.disappear()
       
class Resource(pygame.sprite.Sprite):
    def __init__ (self, x, y, rtype='wood'):
        self.rtype=rtype
        if rtype=="wood":
            imgfile="6wood.png"
            (sizex, sizey)=(15,15)
            
        elif rtype=="hut":
            imgfile="hut.jpg"
            (sizex,sizey)=(50,50)
     
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('images',imgfile)).convert()
        img = pygame.transform.scale(img,(sizex, sizey))
        img.convert_alpha()     # optimise alpha
        if rtype=="wood":
            img.set_colorkey(ALPHA) # set alpha
        elif rtype=="hut":
            img.set_colorkey(WALPHA)
        self.image = img
        self.x=x
        self.y=y
        self.rect  = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.sizey=sizey
        self.sizex=sizex
        
    def disappear(self):
        self.rect.x=-100
        self.rect.y=-100

class platform_game():
    
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.init()
        self.bestscore = 0                                                                                                            
        self.world    = pygame.display.set_mode([screenx,screeny])

    def setup(self,lvl=1):
        self.lvl=1
        if lvl==1:
            wood_piles=200
            px=random.randint(0,worldx)
            py=random.randint(0,worldy)
        self.background=Background(0,0,"Background1.jpg")    
        self.player=Player(px, py)
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)
        self.rlist=pygame.sprite.Group()
        for i in range(wood_piles):
            wx=random.randint(0,worldx)
            wy=random.randint(0,worldy)
            wood=Resource(wx,wy)
            self.rlist.add(wood)
        
        

    
    
    def playgame(self):
        main=True
      
        while main == True:
          
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("gameover, your score is " +str(int(self.player.score)))
#                    pygame.quit(); sys.exit()
                    main = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.player.control(-steps,0)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.control(steps,0)
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.player.control(0,-steps)
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.control(0,steps)
                    if event.key == ord('q'):
                        main=False
                    if event.key == ord('b'):
                        if self.player.wood_carried>=20:
                            hut=Resource(self.player.rect.x,self.player.rect.y,rtype="hut")
                            self.rlist.add(hut)
                            self.player.wood_carried-=20
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.player.control(steps,0)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.control(-steps,0)
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.player.control(0,steps)
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.control(0,-steps)
                        
            if self.player.rect.x>=forwardx:
                #scroll right
                scrollx=self.player.rect.x-forwardx
                self.player.rect.x=forwardx
                self.background.x-=scrollx
                for r in self.rlist:
                    r.rect.x-=scrollx
                    
            if self.player.rect.x<=backwardx:
                #scroll left
                scrollx=self.player.rect.x-backwardx
                self.player.rect.x=backwardx
                self.background.x-=scrollx
                for r in self.rlist:
                    r.rect.x-=scrollx
            if self.player.rect.y>=forwardy:
                #scroll down
                scrolly=self.player.rect.y-forwardy
                self.player.rect.y=forwardy
                self.background.y-=scrolly
                for r in self.rlist:
                    r.rect.y-=scrolly
            if self.player.rect.y<=backwardy:
                #scroll up
                scrolly=self.player.rect.y-backwardy
                self.player.rect.y=backwardy
                self.background.y-=scrolly
                for r in self.rlist:
                    r.rect.y-=scrolly
#            print(self.background.x,self.background.y)
            self.world.blit(self.background.img,[self.background.x,self.background.y])
            self.player_list.update(self.background,self.rlist)
            self.player_list.draw(self.world) # draw player
            self.rlist.draw(self.world)
            largeFont=pygame.font.SysFont("arial",15)
            icons=pygame.sprite.Group()
            if self.player.wood_carried>0:
                wood_icon=Resource(5,5)
                icons.add(wood_icon)
                icons.draw(self.world)
                text=largeFont.render( str(int(self.player.wood_carried)),1,BLACK)
                self.world.blit(text,(18,5))
            self.clock.tick(fps)
            pygame.display.flip()
            self.player.score-=1/fps
            
    def instructions(self):
        return
    
    def entername (self):
        main=True
        name=""
        abc=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']
        while main ==True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();sys.exit()
                    main = False
                if event.type == pygame.KEYDOWN:
                    main=False
                    for ch in abc:
                        if event.key==ord(ch):
                            name+=ch
                            main=True
                            
                        
            self.world.fill(PURPLE)
            largeFont=pygame.font.SysFont("arial",35)
            text=largeFont.render("enter your name",1,WHITE)
            self.world.blit(text,(50,50))
            smallFont=pygame.font.SysFont("freemono",30)
            text=smallFont.render(">" +name,0,WHITE)
            self.world.blit(text,(50,100))
            pygame.display.flip()
            self.clock.tick(fps)
        return name
    
    def menu(self):
        
#bestscores=loadscores(filename)
        main=True
        name=""
       
        lvl=1
        while main == True:
            try:
                score = int (self.player.score)
                if score > self.bestscore:
                    self.bestname=name
                    self.bestscore=score
                bestscore=int (self.bestscore)
                bestname=self.bestname
            except:
                bestscore = 0
                bestname = ""
                score = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                    main = False
                if event.type == pygame.KEYDOWN:
                    if event.key == ord('e'):
                        print("enter name")
                        name=self.entername()
                    if event.key == ord ('i'):
                        print('instructions')
                        self.instructions()
                    if event.key == ord('p'):
                        print('play')
                        pygame.event.clear()
                        mygame.setup(lvl=lvl)
                        self.playgame()
#                        bestscores=playgame(bestscores,name=name)
                    if event.key == ord('q'):
#                        savescores(filename,bestscores)
                        pygame.quit()
                        sys.exit()
                        main=False
            self.world.fill(ORANGE)
            largeFont=pygame.font.SysFont("arial",35)
            text=largeFont.render("Build Your Empire by Evelyn Hyland ",1,WHITE)
            self.world.blit(text,(350,50))
            text=largeFont.render("(P)lay ",0,WHITE)
            self.world.blit(text,(200,200))
            text=largeFont.render("(Q)uit",1,WHITE)
            self.world.blit(text,(200,150))
            text=largeFont.render("(I)nstructions",0,WHITE)
            self.world.blit(text,(200,250))
            text=largeFont.render("(E)nter Name",0,WHITE)
            self.world.blit(text,(200,300))
            text=largeFont.render("Good luck "+name+"!",1,WHITE)
            self.world.blit(text,(200,500))
            text=largeFont.render("Most recent score "+str(score),1,WHITE)
            self.world.blit(text,(700,250))
            text=largeFont.render("Highest score "+str(bestscore)+" by "+bestname,1,WHITE)
            self.world.blit(text,(700,300))
            text=largeFont.render("(L)evel",0,WHITE)
            self.world.blit(text,(200,350))
        
            pygame.display.flip()
            self.clock.tick(fps)

lvl=1
mygame=platform_game()
mygame.menu()
mygame.setup(lvl=lvl)
mygame.playgame()