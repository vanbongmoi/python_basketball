import pygame
import dbconnect as dbconnect
import dbconnecthost as dbconnecthost
import myrequests as myrequests
import RPi.GPIO as GPIO
import time
import threading
import random
import datetime
coin = 5
atick=9
stick=6
led=11
shutd=12
enableticket=13
sen1=4
sen2=17
sen3=14
sen4=15
sen5=18
sen6=23
sen7=24
sen8=25
sen9=19
sen10=26
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(sen1,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(sen2,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(sen3,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(sen4,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(sen5,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(sen6,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(sen7,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(sen8,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(sen9,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(sen10,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(coin,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(stick,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(atick,GPIO.OUT)
GPIO.setup(led,GPIO.OUT)
GPIO.setup(enableticket,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(shutd,GPIO.IN,GPIO.PUD_UP)
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsans',150,True)
font1 = pygame.font.SysFont('comicsans',120,True)
fontrd = pygame.font.SysFont('comicsans',300,True)
fonths = pygame.font.SysFont('comicsans',400,True)
win =pygame.display.set_mode((1360,768),pygame.NOFRAME)
pygame.mouse.set_visible(False)
#pygame.display.set_caption("VLM Basketball")
playing  = pygame.image.load('/home/pi/basketball/images/playing.png')
ready  = pygame.image.load('/home/pi/basketball/images/ready.png')
ticket  = pygame.image.load('/home/pi/basketball/images/ticket.png')
thanks  = pygame.image.load('/home/pi/basketball/images/thanks.png')
ro = pygame.image.load('/home/pi/basketball/images/ro.png')
ball = pygame.image.load('/home/pi/basketball/images/ball.png')
imghighscore = pygame.image.load('/home/pi/basketball/images/highscore.png')
tingting =pygame.mixer.Sound('/home/pi/basketball/ting.wav')
tinidiem = pygame.image.load('/home/pi/basketball/images/tk.png')
tk1 = pygame.image.load('/home/pi/basketball/images/tk1.png')
tk2 = pygame.image.load('/home/pi/basketball/images/tk2.png')
e1 = pygame.image.load('/home/pi/basketball/images/e1.png')
e2 = pygame.image.load('/home/pi/basketball/images/e2.png')
e3 = pygame.image.load('/home/pi/basketball/images/e3.png')
e4 = pygame.image.load('/home/pi/basketball/images/e4.png')
e5 = pygame.image.load('/home/pi/basketball/images/e5.png')
hd1 = pygame.image.load('/home/pi/basketball/huongdanimg/1.png')
hd2 = pygame.image.load('/home/pi/basketball/huongdanimg/2.png')
hd3 = pygame.image.load('/home/pi/basketball/huongdanimg/3.png')
hd4 = pygame.image.load('/home/pi/basketball/huongdanimg/4.png')
listeffect=[]
lsconfig = []
lsconfig = dbconnect.getallconfig()
class Myeffect(object):
    def __init__(self,x,y,img):        
        self.x = x
        self.y = y 
        self.image = img 
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
class Mytinidiem(object):
    def __init__(self,x,y,vel,img):        
        self.x = x
        self.y = y        
        self.vel = vel
        self.image = img        
        self.Startmove=False
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
    def Movedown(self):
        if self.Startmove:
            if self.y <390:            
                self.y +=self.vel
            else:            
                self.y=-300
        else:            
                self.y=-1000
class Myball(object):
    def __init__(self,x,y,vel,img):        
        self.x = x
        self.y = y        
        self.vel = vel
        self.image = img        
        self.Startmove=False
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
    def Movedown(self):
        if self.y <390:            
            self.y +=self.vel
        else:
            self.Startmove=False
            self.y=-150
class Myimage(object):
    def __init__(self,x,y,vel,img):        
        self.x = x
        self.y = y        
        self.vel = vel
        self.image = img
        self.Stop=False
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))

    def Moveup(self):
        if self.y > -768:
            self.y -=self.vel
        else:
            self.Stop=True

    def Movedown(self):
        if self.y < -76:            
            self.y +=self.vel
        else:
            self.Stop=True
class Mydemo(object):
    def __init__(self,x,y,vel,img):        
        self.x = x
        self.y = y        
        self.vel = vel
        self.image = img
        self.Stop=False
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))

    def Moveup(self):
        if self.y > -768:
            self.y -=self.vel
        else:
            self.Stop=True

    def Movedown(self):
        if self.y < -76:            
            self.y +=self.vel
        else:
            self.Stop=True
            
class Playerinfo(object):
    def __init__(self):
        self.Ticket=0
        self.Start = False
        self.Readticket = 0
class Sensor(object):
    def __init__(self):
        self.Isstart=False
        self.Sen1 =False
        self.Sen2 =False
        self.Sen3 =False
        self.Sen4 =False
        self.Sen5 =False
        self.SSen1 =0
        self.SSen2 =0
        self.SSen3 =0
        self.SSen4 =0
        self.SSen5 =0
        self.PSen1 =0
        self.PSen2 =0
        self.PSen3 =0
        self.PSen4 =0
        self.PSen5 =0
class Player(object):   
    def __init__(self):        
        self.Playtime = 0
        self.Coin=0
        self.Point = 0
        self.Device = 0
        self.Ticket = 0
        self.Enableticket = False
        self.Score=0
        self.Highscore=0
        
class Config(object):   
    def __init__(self):     
        self.Coin = 0    
        self.Showtime = '00 : 00'
        self.Countplaytime = 0
        self.Showscore = '00'
        self.Showticket = '00'
        self.Isready = False
        self.Isstart = False
        self.Isticket = False
        self.Readytime = 0
        self.Starttime = 0
        self.Tickettime = 0
        self.Readycount = 5
        self.Ticketcount = 5
        self.Startdelay = False
        self.Startdelayticketup = False
        self.Startdelayticket = False
        self.Startdelaygameover = False
        self.Starthold=False
        self.Holdtime=0
        self.Isdemo = False
        self.demomoveimgtime=0
        self.Countshutdown=0
        self.Nextimg=False
        self.Nextimg1=False
        self.Nextimg2=False
        self.Nextimg3=False
        self.Nextimg4=False
        self.Nextimg5=False
        self.Nextimg6=False
        self.Nextimg7=False
        
myconfig = Config()
myplaying = Myimage(0,0,10,playing)
myticket = Myimage(0,-768,76.8,ticket)
myready = Myimage(0,-768,76.8,ready)
mythank = Myimage(0,-768,76.8,thanks)
myball1 = Myball(90,-150,50,ball)
myball2 = Myball(360,-150,50,ball)
myball3 = Myball(630,-150,50,ball)
myball4 = Myball(895,-150,50,ball)
myball5 = Myball(1165,-150,50,ball)
mytickets = Mytinidiem(600,-1000,50,tinidiem)
odiemtop = Mytinidiem(500,-500,50,tk1)
odiembottom = Mytinidiem(500,-500,50,tk2)
myplayer = Player()
sensor = Sensor()
dbconfig = lsconfig[0]
sensor.PSen1 = dbconfig[5]
sensor.PSen2 = dbconfig[6]
sensor.PSen3 = dbconfig[7]
sensor.PSen4 = dbconfig[8]
sensor.PSen5 = dbconfig[9]
centercode = dbconfig[12]
zonecode=dbconfig[11]
myplayer.Playtime = dbconfig[1]
myplayer.Coin = dbconfig[2]
myplayer.Device = dbconfig[3]
ef1 = Myeffect(0,-130,e1)
ef2 = Myeffect(0,-130,e2)
ef3 = Myeffect(0,-130,e3)
ef4 = Myeffect(0,-130,e4)
ef5 = Myeffect(0,-130,e5)
listeffect.append(ef1)
listeffect.append(ef2)
listeffect.append(ef3)
listeffect.append(ef4)
listeffect.append(ef5)
myhd1 = Mydemo(0,-768,76.8,hd1)
myhd2 = Mydemo(0,-768,76.8,hd2)
myhd3 = Mydemo(0,-768,76.8,hd3)
myhd4 = Mydemo(0,-768,76.8,hd4)
myhd5 = Mydemo(0,-768,76.8,imghighscore)
ro1score=''
ro2score=''
ro3score=''
ro4score=''
ro5score=''
global issendmail
issendmail=False
def Checktimesendmail():    
    curtime = datetime.datetime.now()
    curhourse = curtime.strftime("%H")
    curminute = curtime.strftime("%M")
    if curhourse == '21' and curminute == '25':
        global issendmail
        if issendmail==False:
            issendmail=True
            myrequests.Autosendreport()
            
# check enable ticket
def Checkenableticket():
    isenable=False
    if GPIO.input(enableticket)==False:
        isenable=True
    else:
        isenable=False
    return isenable
myplayer.Enableticket=Checkenableticket()
def Loadhighscore():
    myplayer.Highscore = dbconnect.Gethighscore()
def Refresheffect():
    time.sleep(.3)
    for e in listeffect:
        if e.y>0:
            e.y=-130

def Redrawwindow():
    myplaying.draw(win)   
    if sensor.SSen1 <10:
        ro1score='0'+str(sensor.SSen1)
    else:
        ro1score=str(sensor.SSen1)
    if sensor.SSen2 <10:
        ro2score='0'+str(sensor.SSen2)
    else:
        ro2score=str(sensor.SSen2)
    if sensor.SSen3 <10:
        ro3score='0'+str(sensor.SSen3)
    else:
        ro3score=str(sensor.SSen3)
    if sensor.SSen4 <10:
        ro4score='0'+str(sensor.SSen4)
    else:
        ro4score=str(sensor.SSen4)
    if sensor.SSen5 <10:
        ro5score='0'+str(sensor.SSen5)
    else:
        ro5score=str(sensor.SSen5)
    txttime  = font.render(str(myconfig.Showtime),1,(255,0,0))  
    txtscore = fontrd.render(str(myconfig.Showscore),1,(255,255,255)) 
    txtticket = fontrd.render(str(myconfig.Showticket),1,(255,0,0))
    txtready = fontrd.render(str(myconfig.Readycount),1,(255,0,0))
    txthigh = fonths.render(str(myplayer.Highscore),1,(255,255,255))
    txtsen1 = font1.render(str(ro1score),1,(255,0,0))
    txtsen2 = font1.render(str(ro2score),1,(255,0,0))
    txtsen3 = font1.render(str(ro3score),1,(255,0,0))
    txtsen4 = font1.render(str(ro4score),1,(255,0,0))
    txtsen5 = font1.render(str(ro5score),1,(255,0,0))
    
    win.blit(txttime,(550,15))   
    win.blit(txtsen1,(100,400))
    win.blit(txtsen2,(367,400))
    win.blit(txtsen3,(637,400))
    win.blit(txtsen4,(905,400))
    win.blit(txtsen5,(1170,400))
    for ef in listeffect:
        ef.draw(win)
    myball1.draw(win)
    myball2.draw(win)
    myball3.draw(win)
    myball4.draw(win)
    myball5.draw(win)
    win.blit(ro,(55,180))      
    mythank.draw(win)
    hspos = 0   
    if myplayer.Score>99:
        hspos=470       
    else:
        hspos=550
    hspos1 = 0   
    if myplayer.Highscore>99:
        hspos1=450       
    else:
        hspos1=550  
    win.blit(txtscore,(mythank.x+hspos,mythank.y+320))
    myhd5.draw(win)    
    win.blit(txthigh,(myhd5.x+hspos1,myhd5.y+230))
    myhd1.draw(win)
    myhd2.draw(win)
    myhd3.draw(win)
    myhd4.draw(win)
    myticket.draw(win)   
    win.blit(txtticket,(myticket.x+960,myticket.y+350))
    odiembottom.draw(win)
    mytickets.draw(win)
    odiemtop.draw(win)
    myready.draw(win)
    win.blit(txtready,(myready.x +620,myready.y+350))
   
    pygame.display.update()
playinfo = Playerinfo()
rungame = True
def Checkreturntick():
    counttime = 5
    check = True
    while check:        
        if counttime<=0:            
            if playinfo.Readticket<1:
                GPIO.output(atick,False)
                playinfo.Start = False                
            check=False
        counttime -=1
        time.sleep(1)
def Returnticket(ticket):
    playinfo.Ticket = ticket
    playinfo.Start = True
    GPIO.output(atick,True)
    checkreturntick = threading.Thread(target = Checkreturntick)
    checkreturntick.start()
    while playinfo.Start:        
        if playinfo.Readticket>=playinfo.Ticket:
            GPIO.output(atick,False)
            playinfo.Start=False            
        if GPIO.input(stick)==False:
            playinfo.Readticket+=1
            time.sleep(.15)
        
def Delaymoveready():
     if myconfig.Startdelay:
        myready.Moveup()
        if myready.Stop:            
            myconfig.Nextimg=False
            myconfig.Nextimg1=False
            myconfig.Nextim2=False
            myconfig.Nextim3=False
            myconfig.Nextimg4=False
            myconfig.Nextimg5=False
            myconfig.Nextimg6=False
            myconfig.Nextimg7=False
            myhd1.Stop=False
            myhd2.Stop=False
            myhd3.Stop=False
            myhd4.Stop=False
            myready.Stop=False
            myconfig.Startdelay = False                
            myconfig.Isready = False
            myconfig.Readycount = 5
            myconfig.Isstart=True
            sensor.Isstart=True
            myconfig.Countplaytime = myplayer.Playtime
            myconfig.Starttime = pygame.time.get_ticks()
        
def Delaymoveticket():
    if myconfig.Startdelayticket:
        myticket.y=0 
        if myplayer.Ticket>0:            
            Returnticket(myplayer.Ticket)#payout ticket            
        myconfig.Startdelayticket = False     
        myconfig.Isticket=True
        myconfig.Tickettime = pygame.time.get_ticks()
def Holdgameover():
    if myconfig.Starthold:
        if pygame.time.get_ticks() - myconfig.Holdtime >3000:
            myconfig.Starthold=False
            myplayer.Ticket = myplayer.Score//myplayer.Device
            dbconnect.Savereport(centercode,zonecode,myplayer.Score,myplayer.Ticket)           
            if myplayer.Enableticket:
                if myplayer.Ticket>0:
                    mytickets.y=-350
                    odiemtop.y =0
                    odiembottom.y=399
                    mythank.y=-746
                    mytickets.Startmove=True
                    myconfig.Startdelayticket=True
                    myticket.Stop = False  
                    if myplayer.Ticket<10:
                        myconfig.Showticket ='0'+str(myplayer.Ticket)
                    else:
                        myconfig.Showticket =str(myplayer.Ticket)
                else:                
                    Resetendgame() 
            else:                
                Resetendgame() 
def Delaymovegameover():
    if myconfig.Startdelaygameover:
        mythank.Movedown()
        if mythank.Stop:            
            myconfig.Starthold=True
            mythank.Stop=False            
            myconfig.Startdelaygameover = False
            myconfig.Holdtime = pygame.time.get_ticks()            

def Delaymoveticketup():
    if myconfig.Startdelayticketup:        
        mytickets.y=-1000
        odiemtop.y =-500
        odiembottom.y=-500
        myticket.Moveup()        
        if myticket.Stop:
            try:                
                dbconnecthost.Savereporthost(centercode,zonecode,myplayer.Score,myplayer.Ticket)
            except:
                pass
            mytickets.Startmove=False
            Resetendgame()
def Resetendgame():
    Loadhighscore()
    myhd5.y=0
    mythank.y=-768
    myconfig.Isstart=False
    myticket.Stop = False
    myconfig.Startdelayticketup = False    
    myconfig.Demomoveimgtime = pygame.time.get_ticks()
    myconfig.Nextimg = True
def CheckCoin():
    if myconfig.Isstart ==False and myconfig.Isready==False:       
        if myconfig.Coin>0:
            myconfig.Isdemo = False
            myconfig.Coin-=1        
            myconfig.Isready=True
            myconfig.Readytime = pygame.time.get_ticks()
            myready.y=0
            myhd5.y = -768
        else:
            myconfig.Isdemo = True           

def Rundemo():
    if myconfig.Isdemo:                    
        myhd5.y=0
        if myconfig.Nextimg:
            if pygame.time.get_ticks() - myconfig.Demomoveimgtime>5000: 
                if myhd1.Stop==False:
                    myhd1.Movedown()
                    if myhd1.Stop:
                        myconfig.Nextimg=False
                        myconfig.Nextimg1=True
                        myconfig.Demomoveimgtime = pygame.time.get_ticks()
        if myconfig.Nextimg1:
            if pygame.time.get_ticks() - myconfig.Demomoveimgtime>5000: 
                myconfig.Nextimg2=True
                myconfig.Nextimg1=False
        if myconfig.Nextimg2:
            if myhd2.Stop==False:
                myhd2.Movedown()
                if myhd2.Stop:
                     myconfig.Demomoveimgtime = pygame.time.get_ticks()
                     myconfig.Nextimg2=False
                     myconfig.Nextimg3=True
                     myhd1.y=-768
                     myhd1.Stop=False
        
        if myconfig.Nextimg3:
            if pygame.time.get_ticks() - myconfig.Demomoveimgtime>5000: 
                myconfig.Nextimg4=True
                myconfig.Nextimg3=False
        if myconfig.Nextimg4:
            if myhd3.Stop==False:
                myhd3.Movedown()
                if myhd3.Stop:
                     myconfig.Demomoveimgtime = pygame.time.get_ticks()
                     myconfig.Nextimg4=False
                     myconfig.Nextimg5=True
                     myhd2.y=-768
                     myhd2.Stop=False
        if myconfig.Nextimg5:
            if pygame.time.get_ticks() - myconfig.Demomoveimgtime>5000:                 
                if myplayer.Enableticket:
                    myconfig.Nextimg6=True
                    myconfig.Nextimg5=False                         
                else:                    
                    myhd3.y = -768
                    myhd3.Stop=False
                    if pygame.time.get_ticks() - myconfig.Demomoveimgtime>10000:
                        myconfig.Demomoveimgtime = pygame.time.get_ticks()
                        myconfig.Nextimg=True
                        myconfig.Nextimg5=False
                
        if myconfig.Nextimg6:
            if myhd4.Stop==False:
                myhd4.Movedown()
                if myhd4.Stop:
                     myconfig.Nextimg6=False
                     myconfig.Nextimg7=True
                     myconfig.Demomoveimgtime = pygame.time.get_ticks()                     
                     myhd3.y = -768
                     myhd3.Stop=False
       
        if myconfig.Nextimg7:
            if pygame.time.get_ticks() - myconfig.Demomoveimgtime>5000:                            
                myhd4.y=-768
                myhd4.Stop=False
            if pygame.time.get_ticks() - myconfig.Demomoveimgtime>10000:
                 myconfig.Demomoveimgtime = pygame.time.get_ticks()
                 myconfig.Nextimg7=False
                 myconfig.Nextimg=True  
    
def Showreadytime():    
    if myconfig.Isready:
        Ressetpoint()
        if myconfig.Readycount >0:            
            if pygame.time.get_ticks() - myconfig.Readytime > 1000:               
                myconfig.Readytime = pygame.time.get_ticks()
                myconfig.Readycount -=1          
        if myconfig.Readycount ==1:
            myconfig.Startdelay = True
            myready.Stop=False            
            
def Rungame():
    if myconfig.Isstart and myconfig.Countplaytime>0:
        if pygame.time.get_ticks() - myconfig.Starttime >1000:
            myconfig.Starttime = pygame.time.get_ticks()
            myconfig.Countplaytime-=1                
        if myconfig.Countplaytime ==0:
            sensor.Isstart=False            
            myconfig.Startdelaygameover = True
            mythank.Stop=False   
        myconfig.Showtime = Changetime(myconfig.Countplaytime)
                
def Changetime(mytime):    
    minut = mytime//60
    sec = mytime - (minut*60)
    sphut=''
    sgiay=''
    if minut<10:
        sphut= '0'+ str(minut)
    else:
        sphut = str(minut)
    if sec<10:
        sgiay = '0'+str(sec)
    else:
        sgiay = str(sec)
    strtime = sphut + ' : ' + sgiay    
    return strtime

def Allowmoveball():
    if sensor.Isstart:        
        if myball1.Startmove:
            myball1.Movedown()            
        if myball2.Startmove:
            myball2.Movedown()            
        if myball3.Startmove:
            myball3.Movedown()            
        if myball4.Startmove:
            myball4.Movedown()           
        if myball5.Startmove:
            myball5.Movedown()            
def Checkgroup1():
    if GPIO.input(sen3)==False: 
        if GPIO.input(sen4)==False:            
            if sensor.Sen1 == False:                
                sensor.Sen1=True
                myball1.Startmove=True
                apoint1 = threading.Thread(target = Addpoint,args=[1])
                apoint1.start() 
            
    if GPIO.input(sen3)==True and GPIO.input(sen4)==True:
        sensor.Sen1=False 
       
def Checkgroup2():
    if GPIO.input(sen2)==False: 
        if GPIO.input(sen5)==False:            
            if sensor.Sen2==False:
                sensor.Sen2=True
                myball2.Startmove=True
                apoint2 = threading.Thread(target = Addpoint,args=[2])
                apoint2.start() 
    if GPIO.input(sen5)==True and GPIO.input(sen2)==True:
        sensor.Sen2=False  
       
def Checkgroup3():
    if GPIO.input(sen6)==False: 
        if GPIO.input(sen7)==False:            
           if sensor.Sen3==False:
               sensor.Sen3=True
               myball3.Startmove=True
               apoint3 = threading.Thread(target = Addpoint,args=[3])
               apoint3.start() 
    if GPIO.input(sen6)==True and GPIO.input(sen7)==True:
        sensor.Sen3=False  
        
def Checkgroup4():
    if GPIO.input(sen1)==False: 
        if GPIO.input(sen8)==False:            
            if sensor.Sen4==False:
                sensor.Sen4=True
                myball4.Startmove=True
                apoint4 = threading.Thread(target = Addpoint,args=[4])
                apoint4.start() 
    if GPIO.input(sen1)==True and GPIO.input(sen8)==True:
        sensor.Sen4=False   
       
def Checkgroup5():
    if GPIO.input(sen9)==False: 
        if GPIO.input(sen10)==False:            
            if sensor.Sen5==False:
                sensor.Sen5=True
                myball5.Startmove=True
                apoint5 = threading.Thread(target = Addpoint,args=[5])
                apoint5.start() 
    if GPIO.input(sen9)==True and GPIO.input(sen10)==True:
        sensor.Sen5=False   
def Checksensor():
    while sensor.Isstart:      
        Checkgroup1()
        Checkgroup2()
        Checkgroup3()
        Checkgroup4()
        Checkgroup5()        
        
def Addpoint(point):
    tingting.play()
    rd = random.randrange(0,5)
    if point ==1:
       sensor.SSen1+= sensor.PSen1
       listeffect[rd].x=myball1.x
       listeffect[rd].y=110
    elif point ==2:
       sensor.SSen2+= sensor.PSen2
       listeffect[rd].x=myball2.x
       listeffect[rd].y=110
    elif point ==3:
       sensor.SSen3+= sensor.PSen3
       listeffect[rd].x=myball3.x
       listeffect[rd].y=110
    elif point ==4:
       sensor.SSen4+= sensor.PSen4
       listeffect[rd].x=myball4.x
       listeffect[rd].y=110
    elif point ==5:
       sensor.SSen5+= sensor.PSen5
       listeffect[rd].x=myball5.x
       listeffect[rd].y=110
       
    myplayer.Score = sensor.SSen1 + sensor.SSen2 + sensor.SSen3 + sensor.SSen4 + sensor.SSen5
    if myplayer.Score<10:
        myconfig.Showscore = '0'+str(myplayer.Score)
    else:
        myconfig.Showscore = str(myplayer.Score)
    destroyef = threading.Thread(target=Refresheffect)
    destroyef.start() 
    time.sleep(.15)
def Ressetpoint():
    myhd1.y = -768
    myhd2.y = -768
    myhd3.y = -768
    myhd4.y = -768
    myhd5.y = -768
    myplayer.Score =0    
    myconfig.Showscore = '0'+str(myplayer.Score)
    myconfig.Showtime = '00 : 00'
    myconfig.Countshutdown = 0
    sensor.SSen1=0
    sensor.SSen2=0    
    sensor.SSen3=0
    sensor.SSen4=0
    sensor.SSen5=0
    Loadhighscore()
def Showticket():    
        if myconfig.Isticket: 
            if myconfig.Ticketcount> 0:
                if pygame.time.get_ticks() - myconfig.Tickettime >1000:
                    myconfig.Tickettime = pygame.time.get_ticks()
                    myconfig.Ticketcount-=1                                   
            else:
                myticket.Stop = False
                myconfig.Startdelayticketup = True
                myconfig.Isticket=False
                myconfig.Ticketcount=5
                myhd5.y=0

def UpdateCoin():
    myconfig.Coin+=myplayer.Coin   
def Postdatatohost():
    while True:        
        myrequests.Sendrequest()
        Checktimesendmail()
        if GPIO.input(shutd)==False:
            myconfig.Countshutdown+=1            
            if myconfig.Countshutdown >1:
                myrequests.Callshutdown()                
        time.sleep(10)
        
def checkcointhead():
    while True:        
        Checksensor()
        if GPIO.input(coin)==False:            
            time.sleep(.3)
            UpdateCoin()        
        time.sleep(.1)
        
myconfig.Demomoveimgtime = pygame.time.get_ticks()
myconfig.Nextimg = True
Ressetpoint()
cointhread = threading.Thread(target=checkcointhead)
cointhread.start()
sendrq = threading.Thread(target=Postdatatohost)
sendrq.start()
while  rungame:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GPIO.output(atick,False)
            GPIO.output(led,False)
            rungame  = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_x:
                UpdateCoin()            
    Rundemo()
    mytickets.Movedown()
    Holdgameover()
    Allowmoveball()
    Delaymovegameover()
    Delaymoveticketup()
    Delaymoveready()
    Delaymoveticket()
    Showticket()        
    Showreadytime()   
    Rungame()
    CheckCoin()    
    Redrawwindow()
    clock.tick(30)
pygame.quit()
                                                                                            