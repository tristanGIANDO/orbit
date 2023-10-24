# coding: utf8
import pygame as pg
from pygame import Vector2 as Vec
from math import sqrt, atan2, cos, sin, pi
 
class Main:
    def __init__(self):
        pg.init()
        self.gameDisplay = pg.display.set_mode((int(WINDOWS.x),int(WINDOWS.y)), pg.HWSURFACE| pg.DOUBLEBUF, 8)
        pg.display.set_caption('Systeme Solaire')
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.K_ESCAPE]) # réduit le nombre d'event clavier à gérer
         
        self.clock = pg.time.Clock() # initie la gestion des FPS
        self.font = pg.font.SysFont("Arial", 14) # initie une police
 
        self.objets = pg.sprite.RenderUpdates() # liste pour contenir les objets créés
        self.G = 6.67e-11 # constante de gravitation
        self.scale = 1000000000 # echelle pour faire rentrer les distances dans la fenetre
        self.date = (2451545.5 - 2451545.5)/365.25 # J2000
        self.center = Vec(WINDOWS.x/2, WINDOWS.y/2)
         
    def update(self, FPS = 60):
        """ boucle principale """
        self.running = True
        while self.running:
            self.date += (1/24)
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
            self.gameDisplay.fill((0,0,0,250)) # rempli l'écran en noir
            self.objets.update() # met a jour les objets de la liste
             
            self.objets.draw(self.gameDisplay) # dessine dans la surface principales les objets
            self.gameDisplay.blit(self.font.render(str(int(self.clock.get_fps()))+" FPS", 1, pg.Color("coral")), (10,10)) # affiche les FPS
            self.gameDisplay.blit(self.font.render(str(round(self.date,2))+" date en jour", 1, pg.Color("coral")), (10,30)) # affiche la date en jour
            pg.display.update() # met a jour le rendu
        pg.quit() # ferme la fenetre
 
class Sun(pg.sprite.DirtySprite):
    def __init__(self, pos, radius, mass, color):
        pg.sprite.DirtySprite.__init__(self)
        main.objets.add(self)
        self.name = "Soleil"
        self.pos = pos
        self.radius = radius/main.scale*10
        self.mass = mass
        self.image = pg.Surface((self.radius*2, self.radius*2), pg.SRCALPHA)
        self.image.fill((255,255,255,0))
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        pg.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
 
    def update(self):
        self.rect.center = self.pos
        main.gameDisplay.blit(main.font.render("Foyer", 1, pg.Color("coral")), self.pos)
         
class Astre(pg.sprite.DirtySprite):
    def __init__(self, name, radius, mass, demi_grand_axe, excentricité, longitude_périhélie, longitude_moyenne, période_révolution, longitude_noeud_ascendant, inclinaison, color=0):
        pg.sprite.DirtySprite.__init__(self)
        main.objets.add(self)
        self.name = name
        print("\n",self.name)
        self.radius = radius / main.scale*1000
        self.mass = mass / main.scale # met à l'echelle la masse
         
        self.a = demi_grand_axe*149597870000 # 1 ua = 149597870000 m
        self.e = excentricité
        self.p = longitude_périhélie
        self.L = longitude_moyenne # (longitude moyenne)
        self.P = self.a*(1-self.e**2) # paramètre de l'ellispe
        self.o = longitude_noeud_ascendant
        self.i = inclinaison
         
        self.n = 2*pi/période_révolution # mouvement moyen ?
        print("moyen_mouvement: ",self.n)
 
        self.dist_périhélie_foyer = self.a*(1-self.e)
        self.périhélie = self.rotate(self.p, Vec(0,0), Vec(0,self.dist_périhélie_foyer))
        print("périhélie: ", self.périhélie)
         
        self.dist_aphélie_foyer = self.a*(1+self.e)
        self.aphélie = self.rotate((self.p+180), Vec(0,0), Vec(0,self.dist_aphélie_foyer))
        print("aphélie: ", self.aphélie)
         
        self.dist_centre_foyer = self.e*self.a       
        self.centre = self.rotate((self.p+180), Vec(0,0), Vec(0,self.dist_centre_foyer))
        print("centre :", self.centre)
         
        self.b = self.a*sqrt(1-self.e**2) # demi-petit axe
        self.demi_petit_axe_1 = self.rotate((self.p+90), Vec(0,0), Vec(0,self.b))
        self.demi_petit_axe_2 = self.rotate((self.p-90), Vec(0,0), Vec(0,self.b))
        print("demi-petit axe: ",self.demi_petit_axe_1, self.demi_petit_axe_2)
 
        # lois de kepler
        self.M = self.anomalie_moyenne()
        self.v = self.anomalie_vraie(self.M, self.e)
        self.r = self.P / (1 + self.e * cos(self.v* pi/ 180)) # rayon vecteur
        print("anomalie moyenne: ", self.M,"\nanomalie vrai: ", self.v, "\nrayon vecteur: ", self.r)
         
        # init première pos
        self.pos = Vec(0,0)
        self.pos.x = self.r * (cos(self.o) * cos(self.v + self.p - self.o) - sin(self.o) * sin(self.v + self.p - self.o) * cos(self.i))
        self.pos.y = self.r * (sin(self.o) * cos(self.v + self.p - self.o) + cos(self.o) * sin(self.v + self.p - self.o) * cos(self.i))
        self.pos_z = self.r * (sin(self.v + self.p - self.o) * sin(self.i))
         
        self.old_pos = list()
        self.color = color
        self.image = pg.Surface((self.radius*2/main.scale, self.radius*2/main.scale), pg.SRCALPHA)
        self.image.fill((255,255,255,0))
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.center = self.pos/main.scale+soleil.pos
        pg.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
 
    def rotate(self, angle, centre, pos):
        angle = angle * pi / 180
        newX = cos(angle)*(pos.x-centre.x)-sin(angle)*(pos.y-centre.y)+centre.x
        newY = sin(angle)*(pos.x-centre.x)+cos(angle)*(pos.y-centre.y)+centre.y
        return Vec(newX, newY)
     
    def anomalie_moyenne(self):
        """ n : moyen mouvement
            L : longitude moyenne
            p: longitude périhélie """
        M = self.n*main.date+self.L-self.p
        if M > 360:
            M-= 360
        elif M < 360:
            M+=360
        return M
     
    def anomalie_vraie(self, M, e):
        """ M : anomalie moyenne en degrées
            e : excentricité """
        a1 = (2 * e - e**3/4) * sin(M*pi/180)
        a2 = 5/4 * e**2 * sin(2*M*pi/180)
        a3 = 13/12 * e**3 * sin(3*M*pi/180)
        v = M + (180/pi) * (a1 +a2 +a3)
        return v
     
    def calc_vitesse(self, old_pos_x, old_pos_y, old_pos_z):
     
        distance_deux_points = sqrt((self.pos.x-old_pos_x)**2+(self.pos.y-old_pos_y)**2+(self.pos_z-old_pos_z)**2)
        vitesse = distance_deux_points / (1/24)
        self.vitesse = round((vitesse / 3600),2)
         
    def update(self):
         
        old_pos_x = self.pos.x
        old_pos_y = self.pos.y
        old_pos_z = self.pos_z
         
        self.M = self.anomalie_moyenne()
        self.v = self.anomalie_vraie(self.M, self.e)
        self.r = self.P / (1 + self.e * cos(self.v* pi / 180)) # rayon vecteur en m
 
        self.pos.x = self.r * (cos(self.o) * cos(self.v + self.p - self.o) - sin(self.o) * sin(self.v + self.p - self.o) * cos(self.i))
        self.pos.y = self.r * (sin(self.o) * cos(self.v + self.p - self.o) + cos(self.o) * sin(self.v + self.p - self.o) * cos(self.i))
        self.pos_z = self.r * (sin(self.v + self.p - self.o) * sin(self.i)) # pas dessiné en 2d, mais utile pour les mesures de disances
 
        self.calc_vitesse(old_pos_x, old_pos_y, old_pos_z)
         
        self.draw_trail()
        self.draw_parameter_ellipse()
         
    def draw_trail(self):
        self.old_pos.append((self.pos.x/main.scale+soleil.pos.x, self.pos.y/main.scale+soleil.pos.y)) # ajoute nouvelle valeur de pos dans une liste
        if len(self.old_pos) >= 2: # si la liste a au minimum 2 element
            pg.draw.lines(main.gameDisplay, self.color, False, self.old_pos) # dessiner une ligne reliant toutes les anciennes pos de l'objet
        self.rect.center = self.pos/main.scale+soleil.pos
 
    def draw_parameter_ellipse(self):
        text = self.name+" "+str(self.vitesse)+" m/s"
        main.gameDisplay.blit(main.font.render(text, 1, pg.Color("coral")), self.pos/main.scale+soleil.pos)
        main.gameDisplay.blit(main.font.render("Périhélie", 1, pg.Color("coral")), soleil.pos+self.périhélie/main.scale)
        main.gameDisplay.blit(main.font.render("Aphélie", 1, pg.Color("coral")), soleil.pos+self.aphélie/main.scale)
        main.gameDisplay.blit(main.font.render("Centre", 1, pg.Color("coral")), soleil.pos+self.centre/main.scale)
        pg.draw.line(main.gameDisplay, self.color, soleil.pos, soleil.pos+self.périhélie/main.scale)
        pg.draw.line(main.gameDisplay, self.color, soleil.pos, soleil.pos+self.aphélie/main.scale)
        pg.draw.line(main.gameDisplay, self.color, soleil.pos, soleil.pos+self.demi_petit_axe_1/main.scale)
        pg.draw.line(main.gameDisplay, self.color, soleil.pos, soleil.pos+self.demi_petit_axe_2/main.scale)
 
if __name__ == "__main__":
 
    WINDOWS = Vec(900, 700) #taille de la fenetre
    main = Main() # init objet world
     
    soleil = Sun(WINDOWS/2, 696340000, 198.9*10e28, pg.Color(250,250,0,250))
    # name, radius(m), mass(kg), demi_grand_axe(au), excentricité(rad), longitude_périhélie(deg), longitude_moyenne(deg), période_révolution(day), longitude_noeud_ascendant, inclinaison, color=0
    mercure = Astre("mercure", 2439700, 3.285*10e23, 0.38709927, 0.20563593, 77.45779628, 252.25032350, 87.969, 48.33076593, 7.0049702, pg.Color(120,120,120,250))
    venus = Astre("venus", 6051800, 4.867*10e23, 0.72333566, 0.00677672, 131.60246718, 181.9709950, 224.7010, 76.67984255, 3.39467605, pg.Color(0,250,250,250))
    terre = Astre("terre", 6371000, 59.736*10e23, 1.00000261, 0.0167086342, 102.93768193, 100.46645683, 365.2421904, 0.0, 0.00001531, pg.Color(0,250,0,250))
    mars = Astre("mars", 3389500, 6.39*10e23, 1.52371034, 0.09339410, -23.94362959, -4.55343205, 686.885, 49.55953891, 1.84969142, pg.Color(250,0,0,250))
     
     
    main.update() # boucle principale