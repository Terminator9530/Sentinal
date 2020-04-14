#Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
import pygame
import random
from os import path
with open("high_score.txt","r") as f:
    high_score=int(f.read())#value is readed as string
width=800
height=700
fps=60
white=(255,255,255)
black=(0,0,0)
red=(200,0,0)
bright_red=(255,0,0)
green=(0,200,0)
bright_green=(0,255,0)
blue=(0,0,255)
yellow=(255,255,0)
pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Sentinel 2.0")
icon=pygame.image.load("img/"+"icon.png")
icon.set_colorkey(white)
pygame.display.set_icon(icon)
clock=pygame.time.Clock()
font_name=pygame.font.match_font('Arial')

#draw text

def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,white)
    text_rect=text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface,text_rect)

#draw lives

def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect=img.get_rect()
        img_rect.x=x+30*i
        img_rect.y=y
        surf.blit(img,img_rect)

#sprite object

class BossMissile(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(missile_img,(20+(level*2),40+(level*2)))
        #self.image.set_colorkey(black)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy=+2
        
    def update(self):
        self.rect.y+=self.speedy
        #kill if it moves off the top of screen
        if self.rect.bottom>height:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(bossList[level-1],(70+(level*2),60+(level*2)))
        self.rect=self.image.get_rect()
        self.radius=int(self.rect.width*0.85/2)
        #print(self.radius)
        self.shield=100
        #pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.x=random.randrange(width-self.rect.width)
        self.rect.y=0
        self.speedy=1
        self.speedx=1
        self.shoot_delay=1000
        self.last_shot=pygame.time.get_ticks()
        self.last_shot=pygame.time.get_ticks()
    def update(self):
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top>height:
            self.speedy=-1
        elif self.rect.top<0:
            self.speedy=1
        if self.rect.x>width:
            self.speedx=-1
        elif self.rect.x<0:
            self.speedx=1
        if pygame.time.get_ticks()-self.last_shot>1000:
            self.shoot()
    def shoot(self):
        now=pygame.time.get_ticks()
        if now-self.last_shot>self.shoot_delay:
            self.last_shot=now
            m=BossMissile(self.rect.centerx,self.rect.bottom)
            all_sprites.add(m)
            missile.add(m)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_img,(60,45))
        self.image.set_colorkey(black)#removes the black back
        self.rect=self.image.get_rect()
        self.radius=20
        #pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.centerx=width/2
        self.rect.bottom=height-10
        self.speedx=0
        self.shield=100
        self.shoot_delay=250
        self.last_shot=pygame.time.get_ticks()
        self.lives=3
        self.hidden=False
        self.hide_timer=pygame.time.get_ticks()
        self.power=1
        self.power_timer=pygame.time.get_ticks()

    def update(self):
        #time out powerups
        if self.power>=2 and pygame.time.get_ticks()-self.power_timer>5000:
            self.power-=1
            self.power_timer=pygame.time.get_ticks()

        # if it is time to unhide
        if self.hidden and pygame.time.get_ticks()-self.hide_timer>1500:
            self.hidden=False
            self.rect.centerx=width/2
            self.rect.bottom=height-10
        self.speedx=0
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx=-5
        if keystate[pygame.K_RIGHT]:
            self.speedx=5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x+=self.speedx
        if self.rect.right>width:
            self.rect.right=width
        if self.rect.left<0:
            self.rect.left=0

    def power_shoot(self):
        self.power+=1
        #print("Power : ",self.power)
        self.power_timer=pygame.time.get_ticks()

    def shoot(self):
        now=pygame.time.get_ticks()
        if now-self.last_shot>self.shoot_delay:
            self.last_shot=now
            if self.power==1:
                bullet=Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif self.power==2:
                bullet1=Bullet(self.rect.left,self.rect.centery)
                bullet2=Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
            else:
                bulletl=Bullet(self.rect.left,self.rect.centery)
                bulletm=Bullet(self.rect.centerx,self.rect.top)
                bulletr=Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bulletl)
                bullets.add(bulletl)
                all_sprites.add(bulletm)
                bullets.add(bulletm)
                all_sprites.add(bulletr)
                bullets.add(bulletr)
        shoot_sound.play()
    
    def hide(self):
        #hide the player temporarily
        self.hidden=True
        self.hide_timer=pygame.time.get_ticks()
        self.rect.center=(width/2,height+200)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig=random.choice(meteor_images)
        self.image_orig.set_colorkey(black)
        self.image=self.image_orig.copy()
        self.rect=self.image.get_rect()
        self.radius=int(self.rect.width*0.85/2)
        #print(self.radius)
        #pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.x=random.randrange(width-self.rect.width)
        self.rect.y=random.randrange(-100,-40)
        self.speedy=random.randrange(1,4)
        self.speedx=random.randrange(-2,2)
        self.rot=0
        self.rot_speed=random.randrange(-8,8)
        self.last_update=pygame.time.get_ticks()
    def rotate(self):
        now=pygame.time.get_ticks()
        if(now-self.last_update)>50:
            self.last_update=now
            self.rot=(self.rot+self.rot_speed)%360
            new_image=pygame.transform.rotate(self.image_orig,self.rot)
            old_center=self.rect.center
            self.image=new_image
            self.rect=self.image.get_rect()
            self.rect.center=old_center
    def update(self):
        self.rotate()
        self.rect.x+=self.speedx
        self.rect.y+=self.speedy
        if self.rect.top>height:
            self.rect.x=random.randrange(width-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedy=random.randrange(1,4)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(bullet,(5,40))
        self.image.set_colorkey(black)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy=-10
        
    def update(self):
        self.rect.y+=self.speedy
        #kill if it moves off the top of sceen
        if self.rect.bottom<0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size=size
        self.image=explosion_anim[self.size][0]
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.frame=0
        self.last_update=pygame.time.get_ticks()
        self.frame_rate=60
    def update(self):
        now=pygame.time.get_ticks()
        if now-self.last_update>self.frame_rate:
            self.last_update=now
            self.frame+=1
            if self.frame==len(explosion_anim[self.size]):
                self.kill()
            else:
                center=self.rect.center
                self.image=explosion_anim[self.size][self.frame]
                self.rect=self.image.get_rect()
                self.rect.center=center

#power ups

class PowerUps(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type=random.choice(['shield','gun'])
        if self.type=='shield':
            self.shield_type=random.choice([0,1,2])
            self.image=power_ups[self.type][self.shield_type]
        else:
            self.image=power_ups[self.type]
        self.image.set_colorkey(black)
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.speedy=2
        
    def update(self):
        self.rect.y+=self.speedy
        #kill if it moves off the top of sceen
        if self.rect.top>height:
            self.kill()

def newMob():
    m=Mob()
    mobs.add(m)

def draw_shield_bar(surf,x,y,pct,color):
    if pct<0:
        pct=0
    bar_length=100
    bar_height=15
    fill=(pct/100)*bar_length
    outline_rect=pygame.Rect(x,y,bar_length,bar_height)
    fill_rect=pygame.Rect(x,y,fill,bar_height)
    if fill<20:
        pygame.draw.rect(surf,red,fill_rect)
    else:
        pygame.draw.rect(surf,color,fill_rect)
    pygame.draw.rect(surf,white,outline_rect,2)


'''
#show ins

def ins(bg,level):
    game=bg[level-1]
    screen.fill(black)
    screen.blit(game,(0,0))
    draw_text(screen,"1.Arrow Keys To Move",64,width/2,height/4)
    draw_text(screen,"2.Space To Fire",22,width/2,height/2)
    home=pygame.image.load(path.join(img_dir,"i2.png")).convert()
    home = pygame.transform.scale(home, (50, 50))
    screen.blit(home,(420,5))
    waiting=True
    while waiting:
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        if(480)>mouse[0]>420 and 50>mouse[1]>0:
            if(click[0]==1):
                waiting=False
        pygame.display.update()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
    return show_gameover(bg,level)
    '''
    
resetScore=0
#show game over screen

def show_gameover():
    global resetScore

    #creating high score
    with open("high_score.txt","r") as f:
        high_score=int(f.read())#value is readed as string
    game=pygame.image.load("img/"+"homeImg.jpg").convert()
    screen.blit(game,(0,0))
    draw_text(screen,"Sentinel 2.0",64,width/2,height/4)
    draw_text(screen,"Arrow Keys To Move , Space To Fire",22,width/2,height/2)
    draw_text(screen,"High Score : "+str(high_score),22,700,10)
    pygame.display.flip()
    waiting=True
    '''
    ins1=pygame.image.load(path.join(img_dir,"i1.png")).convert()
    ins2=pygame.image.load(path.join(img_dir,"i2.png")).convert()
    ins1.set_colorkey(black)#this will prevent white color from being blit
    ins2.set_colorkey(black)#this will prevent white color from being blit
    ins1 = pygame.transform.scale(ins1, (50, 50))
    ins2 = pygame.transform.scale(ins2, (50, 50))
    cart=pygame.image.load(path.join(img_dir,"cart.png")).convert()
    cart.set_colorkey(black)#this will prevent white color from being blit
    cart = pygame.transform.scale(cart, (50, 50))
    screen.blit(ins1,(420,5))
    screen.blit(cart,(0,0))
    '''
    while waiting:
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        #print(mouse)
        #print(click)
        '''if(480)>mouse[0]>420 and 50>mouse[1]>0:
            if(click[0]==1):
                screen.blit(ins2,(420,5))
                ins(bg,level)
            else:
                screen.blit(ins1,(420,5))
                '''
        x=350
        y=450
        if(x+100)>mouse[0]>x and (y+50)>mouse[1]>y:
            pygame.draw.rect(screen,bright_green,(x,y,100,50))
            if(click[0]==1):
                waiting=False
        else:
            pygame.draw.rect(screen,green,(x,y,100,50))
        if (x+100)>mouse[0]>x and ((y+70)+50)>mouse[1]>(y+70):
            pygame.draw.rect(screen,bright_red,(x,(y+70),100,50))
            if(click[0]==1):
                pygame.quit()
        else:
            pygame.draw.rect(screen,red,(x,(y+70),100,50))
        if(x+100)>mouse[0]>x and ((y+140)+50)>mouse[1]>(y+140):
            pygame.draw.rect(screen,(10, 117, 240),(x,(y+140),100,50))
            if(click[0]==1):
                with open("high_score.txt","w") as f:
                    f.write(str(0))#high score is reset in text file
                    waiting=False
                    resetScore=1
                draw_text(screen,"High Score : "+str(0),22,700,10)
        else:
            pygame.draw.rect(screen,(5, 72, 150),(x,(y+140),100,50))
        draw_text(screen,"Start",40,x+50,y)
        draw_text(screen,"Exit",40,x+50,y+70)
        draw_text(screen,"Reset",40,x+50,y+140)
        pygame.display.update()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
    if resetScore:
        resetScore=0
        show_gameover()

#show game over screen

def show_pause():
    game=pygame.image.load("img/"+"homeImg.jpg").convert()
    screen.blit(game,(0,0))
    draw_text(screen,"Pause",64,width/2,height/4)
    draw_text(screen,"Press any key to resume",22,width/2,height/2)
    pygame.display.flip()
    waiting=True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                waiting=False

#credit screen

def credit():
    content=['         Credits         ','Designed By : ','1.Vaibhav Shukla','2.Siddharth Mishra','3.Vaibhav Raj Mishra','4.Siddhartha Srivastava']
    height_credit=700
    flag=0
    while (height_credit+400)>=0:
        screen.fill((68, 68, 68))
        draw_text(screen,content[0],30,width/2,height_credit)
        draw_text(screen,content[1],30,width/2,height_credit+70)
        draw_text(screen,content[2],30,width/2,height_credit+140)
        draw_text(screen,content[3],30,width/2,height_credit+210)
        draw_text(screen,content[4],30,width/2,height_credit+280)
        draw_text(screen,content[5],30,width/2,height_credit+350)
        height_credit-=1
        pygame.display.update()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                height_credit=-400
    while not flag:
        screen.fill((68, 68, 68))
        draw_text(screen,"The End",40,width/2,height/4)
        draw_text(screen,"Press any key to restart the game",30,width/2,height/2)
        pygame.display.update()
        clock.tick(fps)
        for event in pygame.event.get():
            #print(event)
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                flag=1
                break
        if flag==1:
            break

#load all game graphics

bg=[]
back_list=['back1.jpg','back2.jpg','back3.jpg','back4.jpg','back5.jpg']
for img in back_list:
    bg.append(pygame.image.load("img/"+img).convert())
player_img=pygame.image.load("img/ship.png").convert()
player_mini=pygame.transform.scale(player_img,(25,19))
player_mini.set_colorkey(black)
bossList=[]
boss_list=['enemyBlue1.png','enemyBlue2.png','enemyBlue3.png','enemyBlue4.png','enemyBlue5.png']
for img in boss_list:
    temp=pygame.image.load("img/"+img).convert()
    temp.set_colorkey(black)
    bossList.append(temp)
missile_img=pygame.image.load("img/"+"rocket.png").convert()
missile_img.set_colorkey(black)#this will prevent white color from being blit
bullet=pygame.image.load("img/"+"laser.png").convert()
meteor_images=[]
meteor_list=['meteor.png','meteor1.png','meteor2.png','meteor3.png','meteor4.png']
power_ups={}
power_ups['shield']=[]
img=pygame.image.load("img/"+'shield_gold.png').convert()
power_ups['shield'].append(img)
img=pygame.image.load("img/"+'shield_silver.png').convert()
power_ups['shield'].append(img)
img=pygame.image.load("img/"+'shield_bronze.png').convert()
power_ups['shield'].append(img)
power_ups['gun']=pygame.image.load("img/"+'bolt_gold.png').convert()

for img in meteor_list:
    meteor_images.append(pygame.image.load("img/"+img).convert())

#Load all game sound

shoot_sound=pygame.mixer.Sound("sound/"+'Laser_Shoot.wav')
expl_sound=pygame.mixer.Sound("sound/"+'explode.wav')
pygame.mixer.music.load("sound/"+'tgfcoder-FrozenJam-SeamlessLoop.ogg')
pygame.mixer.music.set_volume(0.4)

#explosion images

explosion_anim={}
explosion_anim['lg']=[]
explosion_anim['sm']=[]
explosion_anim['player']=[]
for i in range(9):
    filename='regularExplosion0{}.png'.format(i)
    img=pygame.image.load("img/"+filename).convert()
    img.set_colorkey(black)
    img_lg=pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm=pygame.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_sm)
    filename='sonicExplosion0{}.png'.format(i)
    img=pygame.image.load("img/"+filename).convert()
    img.set_colorkey(black)
    explosion_anim['player'].append(img)

asteroid=0
level=1
running=True
game_over=True
pause=False
end=0
score=0
pygame.mixer.music.play(-1)

while running:
    if game_over:
        if score>high_score:
            high_score=score
        with open("high_score.txt","w") as f:
            f.write(str(high_score))#value is written in text file
        show_gameover()
        game_over=False
        
        #sprite grp

        all_sprites=pygame.sprite.Group()
        mobs=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        missile=pygame.sprite.Group()
        bosses=pygame.sprite.Group()
        powerups=pygame.sprite.Group()
        player=Player()
        all_sprites.add(player)

        for i in range(8+level*2):
            newMob()
        score=0
        count=0
        asteroid=0
        flag=0
        level=1
        end=0
    if pause:
        show_pause()
        pause=False
    #keep loop running at the right speed

    clock.tick(fps)

    #process input(events)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                pause=True


    #check to see if mob hit player

    hits=pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
    for hit in hits:
        if hit.radius==18:
            player.shield-=40
            newMob()
        else:
            player.shield-=80
            newMob()
        if player.shield<=0:
            #print("Collision")
            death_explosion=Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            expl_sound.play()
            player.hide()
            player.lives-=1
            player.shield=100

    #collision  check if the player hit a power up( if the player hit the powerup the power up dissappears as it is true)

    hits=pygame.sprite.spritecollide(player,powerups,True,pygame.sprite.collide_circle)
    for hit in hits:
        if hit.type=='shield':
            if hit.shield_type==0:
                player.shield+=30
            elif hit.shield_type==1:
                player.shield+=20
            else:
                player.shield+=10
            if player.shield>=100:
                player.shield=100 
        if hit.type=='gun':
            player.power_shoot()

    #give time for explosion to play

    if player.lives==0 and not death_explosion.alive():
        #print("Game Over")
        game_over=True
    
    #check if the bullet hit the mob

    bullhit=pygame.sprite.groupcollide(mobs,bullets,True,True)
    for h in bullhit:
        count+=1
        #print("Count : ",count)
        if(count<=20):
            if(h.radius==18):
                score+=2
                expl=Explosion(h.rect.center,'sm')
                all_sprites.add(expl)
                expl_sound.play()
                #10% chance of spawning a power up when small asteroid is destroyed
                if random.random()>0.7:
                    power=PowerUps(h.rect.center)
                    all_sprites.add(power)
                    powerups.add(power)
            else:
                score+=5
                expl=Explosion(h.rect.center,'lg')
                all_sprites.add(expl)
                expl_sound.play()
                #30% chance of spawning a power up when big asteroid is destroyed
                if random.random()>0.8:
                    power=PowerUps(h.rect.center)
                    all_sprites.add(power)
                    powerups.add(power)
            newMob()
        elif count==21:
            boss=Boss()
            bosses.add(boss)
            flag=1
            mobs.empty()
    
    #check if the bullet hit the boss

    boss_hit=pygame.sprite.groupcollide(bosses,bullets,False,True)
    for h in boss_hit:
        asteroid+=1
        score+=100
        boss.shield=boss.shield-(11-level*2)
        if random.random()>0.9:
            power=PowerUps(h.rect.center)
            all_sprites.add(power)
            powerups.add(power)
        if asteroid%10==0:
            for i in range(1):
                newMob()
        if boss.shield<0:
            flag=0
            level+=1
            for i in range(8+level*2):
                newMob()
            count=0
            if level>5:
                flag=1
                level=5
                end=1
            explode=Explosion(boss.rect.center,'player')
            all_sprites.add(explode)
            expl_sound.play()
            bosses.empty()
            bullets.empty()
            missile.empty()
            bosses.update()
            bullets.update()
            missile.update()
            all_sprites.update()

    if end==1 and flag==1 and boss.shield<0 and not explode.alive():
        pygame.time.delay(1500)
        game_over=True
        flag=0
        credit()
        continue

    #check to see if boss hit player

    hits=pygame.sprite.spritecollide(player,bosses,False,pygame.sprite.collide_circle)
    for hit in hits:
        player.shield-=10
        if player.shield<=0:
            #print("Collision")
            death_explosion=Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            expl_sound.play()
            player.hide()
            player.lives-=1
            player.shield=100

    if player.lives==0 and not death_explosion.alive():
        #print("Game Over")
        game_over=True

    #check if the missile hit the player

    bullhit=pygame.sprite.spritecollide(player,missile,True)
    for h in bullhit:
        player.shield-=30
        if player.shield<0:
            expl=Explosion(h.rect.center,'player')
            all_sprites.add(expl)
            expl_sound.play()
            player.hide()
            player.lives-=1
            player.shield=100


    if player.lives==0 and not expl.alive():
        #print("Game Over")
        game_over=True

    #check if the missile hit the bullets

    bullhit=pygame.sprite.groupcollide(bullets,missile,True,True)

    #update

    all_sprites.update()
    mobs.update()
    bosses.update()
    missile.update()


    #draw
    screen.fill(black)
    screen.blit(bg[level-1],(0,0))
    #pygame.draw.ellipse(screen, yellow, (0, height-120, width, 200), 0) 
    all_sprites.draw(screen)
    mobs.draw(screen)
    bosses.draw(screen)
    draw_text(screen,"Score : "+str(score),18,width/2-50,10)
    draw_text(screen,"Level : "+str(level),18,width/2+50,10)
    draw_text(screen,"Player  ",15,20,5)
    draw_shield_bar(screen,40,5,player.shield,(9, 227, 49))
    if flag==1:
        draw_shield_bar(screen,40,25,boss.shield,(9, 209, 227))
        draw_text(screen,"Boss    ",15,20,25)
    draw_lives(screen,width-100,5,player.lives,player_mini)
    #draw_text(screen,str(player.shield),18,120,5)

    #after drawing everything flip the display

    pygame.display.flip()