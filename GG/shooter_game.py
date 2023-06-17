#Створи власний Шутер!

from pygame import *

from pygame import *
from random import *

height=700
width=500

window=display.set_mode((height,width))
display.set_caption("Shooter")
background=transform.scale(image.load("galaxy.jpg"),(700,500))
clock=time.Clock()
FPS=60

font.init()
font2=font.Font(None,36)
lost=0
score=0
max_lost=3

win = font2.render("YOU WIN",True,(255,255,255))
lose = font2.render("YOU LOSE",True,(255,255,255))

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image=transform.scale(image.load(player_image),(size_x,size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def move(self):
        key_pressed=key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x <= 600 :
            self.rect.x+=self.speed 
        if key_pressed[K_LEFT] and self.rect.x >= 5 :
            self.rect.x-=self.speed
    
    def fire(self):
        bullet=Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global lost
        if self.rect.y>height:
            self.rect.x=randint(80,width-80)
            self.rect.y=0
            lost=lost+1


class Bullet(GameSprite):
    def update(self):
        self.rect.y+=self.speed

        if self.rect.y<0:
            self.kill()


img_monster = "ufo.png"
monsters=sprite.Group()
for i in range(1,6):
    monster=Enemy(img_monster,randint(80,width-80),-40,80,50,randint(1,5))
    monsters.add(monster)

bullets=sprite.Group()
player=Player("rocket.png",100,400,65,65,10)
game=True
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

shoot=mixer.Sound('fire.ogg')
finish=False
while game:
    
    for e in event.get():
        if e.type==QUIT:
            game=False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                shoot.play()
                player.fire()
    if not finish:
        
        window.blit(background,(0,0))
        text=font2.render("Пропуски:"+str(lost),1,(255,255,255))
        window.blit(text,(10,20))
        monsters.update()
        text2=font2.render("Рахунок:"+str(score),1,(255,255,255))
        window.blit(text2,(10,70))
        bullets.update()
        player.reset()
        
        monsters.draw(window)
        bullets.draw(window)
        player.move()
        collidergroup= sprite.groupcollide(bullets , monsters , True,True)
        for c in collidergroup :
            score = score + 1
            monster=Enemy(img_monster,randint(80,width-80),-40,80,50,randint(1,5))
            monsters.add(monster)
        
        if sprite.spritecollide(player,monsters,False) or lost >= max_lost :
            finish = True
            window.blit(lose,(250 , 250))
        
        if score >= 10 :
            finish = True
            window.blit(win,(250 , 250))
         
        
    display.update()
    clock.tick(FPS)