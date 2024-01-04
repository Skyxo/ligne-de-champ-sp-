from math import *

width, height = 900, 900
eps0 = 8.85418782*10**(-12) # m-3 kg-1 s4 A2
k = 1/(4*pi*eps0)
e = 1.6*10**(-19)
nbvect = 25

class Particule:
    
    def __init__(self, x, y, q):
        self.x = x
        self.y = y
        self.q = q
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getQ(self):
        return self.q
    
    def drawParticule(self):
        q = self.getQ()
        
        if q>0:
            fill(255,0,0)
        if q<0:
            fill(0,0,255)

        circle(self.getX(), self.getY(), 10*sqrt(abs(self.getQ()/e)))
    
    def getChampFrom(self, xp, yp):
        MP = sqrt((xp-self.getX())**2 + (yp-self.getY())**2)

        if MP > 0:
            Ex = k*self.getQ()*(xp-self.getX())/(MP**3)
            Ey = k*self.getQ()*(yp-self.getY())/(MP**3)
        else:
            Ex, Ey = 0, 0
            
        return Ex, Ey

class Fleche():
    
    def __init__(self, posx, posy, cx, cy):
        self.posx = posx
        self.posy = posy
        self.champx = cx
        self.champy = cy
        
    def getPosX(self):
        return self.posx
    
    def getPosY(self):
        return self.posy
    
    def getChampX(self):
        return self.champx
    
    def getChampY(self):
        return self.champy
    
    def setChamp(self, x, y):
        self.champx = x
        self.champy = y
    
    def drawArrow(self):
        x, y = self.getPosX(), self.getPosY()
        cx, cy = self.getChampX(), self.getChampY()
        d = sqrt(cx**2 + cy**2)
        
        if d>0:
            tox = (width/nbvect)*cx/d
            toy = (height/nbvect)*cy/d
        else:
            tox, toy = 0, 0
        
        line(x, y, x+tox, y+toy)
        a = (height+width)/(2*nbvect)/15
        fill(0,0,0)
        pushMatrix()
        angle = atan2(toy-cy, tox-cx)
        translate(x+tox, y+toy)
        rotate(angle)
        triangle(- a * 2 , - a, 0, 0, - a * 2, a)
        popMatrix()
        
        
def posVect(n):
    
    pos = [[0 for j in range(nbvect+1)] for i in range(nbvect+1)]

    for i in range(nbvect+1):
        for j in range(nbvect+1):
            pos[i][j] = (i*width/n, j*height/n)
        
    return pos

def createArrows(n):
    posvect = posVect(n)
    
    for ligne in posvect:
        for v in range(len(ligne)):
            ligne[v] = Fleche(ligne[v][0], ligne[v][1], ligne[v][0], ligne[v][1])
            
    return posvect
    
def refreshArrows(particules):
    global arrows
    
    for ligne in arrows:
        for arrow in ligne:
            champx = 0
            champy = 0
                        
            for p in particules:
                Ex, Ey = p.getChampFrom(arrow.getPosX(), arrow.getPosY())
                champx+=Ex
                champy+=Ey
            
            arrow.setChamp(champx, champy)
    
arrows = createArrows(nbvect)
hud = 1

p1 = Particule(75,200,3*e)
p2 = Particule(500,700,-3*e)

qmouse=0
particules = []
    
def setup():
    size(width, height)
    
def draw():
    global arrows
    background(0)
    #background(150,255,255)
    fill(255,0,0)
    stroke(255)
    
    if qmouse:
        sp = Particule(mouseX, mouseY, qmouse*e)
        particules.append(sp)
    
    refreshArrows(particules)
    
    for ligne in arrows:
        for arrow in ligne:
            arrow.drawArrow()
            
    for p in particules:
        p.drawParticule()   
    
    if hud:
        textSize(20)
        fill(255)
        text("P : Positif\nN : Negatif\nO : Montre charge\nUP/DOWN : Taille charge\nLEFT/RIGHT : nbVecteurs\nClick : Depose une charge", 10, 20)
    
    if qmouse:   
        particules.remove(particules[-1])
            
def mouseClicked():
    global particules
    particules.append(Particule(mouseX, mouseY, qmouse*e))
    print("Particule de charge {}eV placee en x={}, y={}".format(qmouse, mouseX, mouseY))
    
def keyPressed():
    global particules, qmouse, nbvect, arrows, hud
    
    if key == "h":
        hud = 0 if hud else 1
    if key == 'p':
        qmouse = abs(qmouse) if qmouse else 1
        print("charge : {}eV".format(qmouse))
    if key == 'n':
        qmouse = -abs(qmouse) if qmouse else -1
        print("charge : {}eV".format(qmouse))
    if key == 'o':
        qmouse = 0 if qmouse else 1
    if keyCode == UP and qmouse!=0:
        qmouse += qmouse/abs(qmouse)
        print("charge : {}eV".format(qmouse))
    if keyCode == DOWN and abs(qmouse) > 1:
        qmouse -= qmouse/abs(qmouse)
        print("charge : {}eV".format(qmouse))
    if keyCode == RIGHT:
        nbvect += 1
        arrows = createArrows(nbvect)
    if keyCode == LEFT and nbvect>1:
        nbvect -= 1
        arrows = createArrows(nbvect)
    
