# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:14:25 2011

@author: Jboeye
"""
max_x=500                                                #Landscape boundaries
max_y=500                                                #Landscape boundaries
maxspeed=3                                               #Maximal speed of species
startpop=100
starttrappop=10
maxpop=200
maxhunger=60
maxtrappop=30
maxage=500
maxradius=20
minradius=4
pmutation=0.05
maturity=20

import random
from math import *                                       #This way you dont have to type math.cos but just cos
import Tkinter as tk
root = tk.Tk()

canvas = tk.Canvas(root, width=max_x, height=max_y)      #create window
canvas.pack()

class Beetle:     
    def __init__(self, angle, x, y, pers_maxspeed,age=0, drawing=None):   #blueprint of beetle
        self.age=age
        self.angle = angle             
        self.x = x
        self.y = y
        self.pers_maxspeed = pers_maxspeed                  #create individual maxspeed
        self.drawing=canvas.create_rectangle(self.x-1, self.y-1, self.x+1, self.y+1, outline='red',fill='red')        

    def move(self):
        self.age+=1
        speed=random.uniform(0,self.pers_maxspeed)
        self.angle += random.uniform(-pi/8,pi/8)
        #This algorithm implements a perceptual range and running from trap
        for a in traps:        #For loop over all traps, can this be avoided?
                if (self.x-a.x)**2+(self.y-a.y)**2<6*(a.radius)**2: #Is a trap vissible (larger traps can be seen from longer distance)
                  speed=self.pers_maxspeed          #They flee as fast as they can
                  self.angle=random.uniform(-pi/4,pi/4) + acos(fabs(self.x-a.x)/(sqrt((self.x-a.x)**2+(self.y-a.y)**2))); # If trap is to the lower left we keep this angle, since we made everything positive the prey runs to the upper right automatically
                  if (self.x-a.x<0) and (self.y-a.y>0): # trap to the lower right
                      self.angle+=pi/2;                 # +90°
                  elif (self.x-a.x<0) and (self.y-a.y<0): # trap to the upper right 
                      self.angle+=pi;                   # +180°
                  elif (self.x-a.x>0) and (self.y-a.y<0): # trap to the upper left
                      self.angle-=pi/2;                 # -90°
                  break #exit the loop if fleeing from 1 trap (so they don't flee from a second)
        #what distance will they move          
        dx = speed * cos(self.angle)
        dy = speed * sin(self.angle)
        #correct movement if landscape boundaries are reached
        if (self.x+dx>max_x):
            dx=max_x-self.x
            self.x=max_x
            self.angle=pi-self.angle
        if (self.x+dx<0):
            dx=-self.x
            self.x=0
            self.angle=pi-self.angle
        if (self.y+dy>max_y):
            dy=max_y-self.y
            self.y=max_y
            self.angle=-self.angle
        if (self.y+dy<0):
            dy=-self.y
            self.y=0
            self.angle=-self.angle
        if (self.x+dx<max_x) and (self.x+dx>0):
            self.x += dx
        if (self.y+dy<max_y) and (self.y+dy>0):
            self.y += dy
            
        #check if caught my trap
        alive=True
        for a in traps:
                if ((self.x-a.x)**2+(self.y-a.y)**2) < ((a.radius)**2):
                    Beetle.death(self)
                    a.eat()
                    alive=False
                    break #exit loop, if caught by one trap can't get cought by second
        #if alive -> reproduce
        if random.random()<self.age/maxage and alive==True:
            Beetle.death(self)
            alive=False
        #draw ultimate movement if alive            
        if alive:
            canvas.move(self.drawing,dx,dy)
        if alive and random.random()>len(beetles)/maxpop and len(nieuw)<maxpop and self.age>maturity:
            Beetle.reproduction(self) 
            
        #reproduce...
    def reproduction(self):
        offspring=[Beetle(self.angle, self.x, self.y, self.pers_maxspeed)]
        global p
        p+=len(offspring)
        nieuw.extend(offspring)
        
        #what to do if trapped
    def death(self):
        canvas.delete(self.drawing)          
        global p
        del nieuw[p]
        p-=1
      
        #canvas.itemconfig(self.drawing, outline='blue', fill="blue")

class Trap:    
    def __init__(self,angle,x,y, radius, pers_maxspeed=0,hunger=0,drawing=None,age=0):
        self.age=0
        self.hunger=0
        self.radius=radius
        if self.radius<0.5:
            self.radius=0.5
        self.pers_maxspeed = 40/self.radius
        self.angle =angle
        self.x = x
        self.y = y
        self.drawing = canvas.create_oval(self.x-self.radius,self.y-self.radius,self.x+self.radius,self.y+self.radius, outline='blue',fill='green')

               
    def move(self):
        self.age+=1
        self.hunger+=1
        speed=random.uniform(0,self.pers_maxspeed)
        self.angle += random.uniform(-pi/8,pi/8)

        for a in beetles:
            if ((self.x-a.x)**2+(self.y-a.y)**2) < ((self.radius)**2)*4:            
                speed=self.pers_maxspeed
                self.angle=random.uniform(-pi/4,pi/4) + acos(fabs(self.x-a.x)/(sqrt((self.x-a.x)**2+(self.y-a.y)**2))); # If trap is to the lower left we keep this angle, since we made everything positive the prey runs to the upper right automatically
                if (self.x-a.x<0) and (self.y-a.y>0): # prey to the lower right
                    self.angle-=pi/2;                 # -90°
                elif (self.x-a.x>0) and (self.y-a.y>0): # prey to the lower left 
                    self.angle+=pi;                   # +180°
                elif (self.x-a.x>0) and (self.y-a.y<0): # trap to the upper left
                   self.angle+=pi/2;                  # +90°  
                break       
     
        
        dx = speed * cos(self.angle)
        dy = speed * sin(self.angle)
        if (self.x+self.radius+dx>max_x):
            dx=max_x-(self.x+self.radius)
            self.x=max_x-self.radius
            self.angle=pi-self.angle
        elif (self.x-self.radius+dx<0):
            dx=-self.x+self.radius
            self.x=self.radius
            self.angle=pi-self.angle
        if (self.y+self.radius+dy>max_y):
            dy=max_y-(self.y+self.radius)
            self.y=max_y-self.radius
            self.angle=-self.angle
        elif (self.y-self.radius+dy<0):
            dy=-self.y+self.radius
            self.y=self.radius
            self.angle=-self.angle
        if (self.x+dx<max_x) and (self.x+dx>0):
            self.x += dx
        if (self.y+dy<max_y) and (self.y+dy>0):
            self.y += dy
        canvas.move(self.drawing,dx,dy)

#        for a in beetles:
#            if ((self.x-a.x)**2+(self.y-a.y)**2) < ((self.radius)**2):
#               self.hunger-=10
#               if self.hunger<0:
#                   self.hunger=0

        if self.hunger>maxhunger:
            Trap.starve(self)
        
        if self.hunger<maxhunger/2 and self.age>maturity and random.random()<0.1 and random.random ()>len(traps)/maxtrappop:
            Trap.reproduction(self)            
            
    def starve(self):
        canvas.delete(self.drawing)          
        global t
        del newtraps[t]
        t-=1     
        
    def eat(self):
        self.hunger-=10
        if self.hunger<0:
            self.hunger=0   
            
    def reproduction(self):
        mutation=0
        if random.random()<pmutation:
            mutation=random.uniform(-2,2)
        offspring=[Trap(self.angle, self.x, self.y, self.radius+mutation)]
        global t
        t+=len(offspring)
        newtraps.extend(offspring)


#PREPARATIONS & INITIALIZATIONS        
beetles = []
traps = []

for i in range (starttrappop):             #Initialize traps
    radius=random.uniform(minradius,maxradius)
    angle = random.uniform(0,2*pi) 
    x = random.uniform(radius,max_x-radius)
    y = random.uniform(radius,max_y-radius)
    traps.append(Trap(angle,x,y,radius))
    
for k in range (startpop):      #initialize beetles
    angle = random.uniform(0,2*pi)             
    x = random.uniform(0,max_x)
    y = random.uniform(0,max_y)
    pers_maxspeed = random.uniform(0.1,maxspeed)                   #create individual maxspeed    
    beetles.append(Beetle(angle,x,y,pers_maxspeed))    

#MAINLOOP
for stap in range(50000):
    p=0
    t=0
    nieuw = []                  #empty newpopulation list
    newtraps = []               #empty new trap population list
    canvas.update()             #update screen
    
    for b in traps:             #move traps
        newtraps.append(b)      
        b.move()
        t+=1
    traps = newtraps
        
    for a in beetles:           #move beetles
        nieuw.append(a)
        a.move()
        p+=1
    beetles = nieuw             #New population becomes oldpopulation


root.mainloop() #halts screen after simulation???

