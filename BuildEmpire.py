import pygame # load pygame keywords
import sys # let python use file system
import os # help python identify your OS
import time
import csv
'''
Variables
'''
ALPHA=(0, 0, 0)
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

screenx=1850
screeny=950
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
      
        
    def control(self,x,y):
        self.movex += x
        self.movey += y
        
    def update(self,bg):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        if self.rect.x -bg.x< backwardx:
#            self.rect.x-=self.movex
            self.rect.x=screenx-backwardx+bg.x
            bg.x=-(worldx-screenx)
        if self.rect.x-bg.x>worldx-backwardx:
#            self.rect.x-=self.movex
            self.rect.x=backwardx
            bg.x=0
        if self.rect.y-bg.y>worldy-backwardy:
            #self.rect.y-=self.movey
            self.rect.y=backwardy
            bg.y=0
        if self.rect.y-bg.y<backwardy:
            #self.rect.y-=self.movey
            self.rect.y=screeny-backwardy+bg.y
            bg.y=-(worldy-screeny)
        
       
      
     

class platform_game():
    
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.init()
        self.bestscore = 0                                                                                                            
        self.world    = pygame.display.set_mode([screenx,screeny])

    def setup(self,lvl=1):
        self.lvl=1
        if lvl==1:
            px=150
            py=int(5*ty)
        self.background=Background(0,0,"Background1.jpg")    
        self.player=Player(px, py)
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)
        

    
    
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
            if self.player.rect.x<=backwardx:
                #scroll left
                scrollx=self.player.rect.x-backwardx
                self.player.rect.x=backwardx
                self.background.x-=scrollx
            if self.player.rect.y>=forwardy:
                #scroll down
                scrolly=self.player.rect.y-forwardy
                self.player.rect.y=forwardy
                self.background.y-=scrolly
            if self.player.rect.y<=backwardy:
                #scroll up
                scrolly=self.player.rect.y-backwardy
                self.player.rect.y=backwardy
                self.background.y-=scrolly
#            print(self.background.x,self.background.y)
            self.world.blit(self.background.img,[self.background.x,self.background.y])
            self.player_list.update(self.background)
            self.player_list.draw(self.world) # draw player
#            largeFont=pygame.font.SysFont("arial",25)
#            text=largeFont.render("Score: "+str(int(self.player.score)),1,WHITE)
#            self.world.blit(text,(10,10))
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