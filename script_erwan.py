from tkinter import *
import random
#Création des dictionnaires
dico_c={}
dico_voeux={}

#Liste qui permet les calculs de durée d'évacuation
L=[]

#initialise la variable qui compte les etape du programme                
compteur_etape=0

#Taille du quadriallage
largeur_quadrillage=600
hauteur_quadrillage=600

#dimensions d'une cellule
c=30

#On place la sortie
x0=300
y0=0
#initialise la variable qui gere la vitesse du programme     
vitesse=1

#Nombre de personne initilaement généré par la fonction qui crée cette foule
nb_personnes=10

#variable qui permet le fonctionnement de la fonction go()
valeur_arret=0


#fonction dessinant le tableau
def damier(): 
    ligne_vert()
    ligne_hor()
        
#crée les lignes verticales du quadriallage        
def ligne_vert():
    c_x = 0
    while c_x != largeur_quadrillage:
        can1.create_line(c_x,0,c_x,hauteur_quadrillage,width=1,fill='black')
        c_x+=c
        
#crée les lignes horizontales du quadriallage        
def ligne_hor():
    c_y = 0
    while c_y != hauteur_quadrillage:
        can1.create_line(0,c_y,largeur_quadrillage,c_y,width=1,fill='black')
        c_y+=c
        
#fonction rendant vivante la cellule cliquée donc met la valeur 1 pour la cellule cliquée au dico_case
def click_gauche(event): 
    x = event.x -(event.x%c)
    y = event.y -(event.y%c)
    can1.create_rectangle(x, y, x+c, y+c, fill='black')
    dico_c[x,y]=1

#fonction rendant vivante la cellule cliquée donc met la valeur 1 pour la cellule cliquée au dico_case    
def click_molette(event): 
    x = event.x -(event.x%c)
    y = event.y -(event.y%c)
    can1.create_rectangle(x, y, x+c, y+c, fill='red')
    dico_c[x,y]=2
    
#fonction tuant la cellule cliquée donc met la valeur 0 pour la cellule cliquée au dico_case
def click_droit(event): 
    x = event.x -(event.x%c)
    y = event.y -(event.y%c)
    can1.create_rectangle(x, y, x+c, y+c, fill='white')
    dico_c[x,y]=0
    
#fonction pour changer la vitesse(l'attente entre chaque étape)    
def change_vit(event):
    global vitesse
    vitesse = int(eval(entree.get())) # permet de modifier la valeur en tapant au clavier
    print("la vitesse est: "+str(vitesse)+"ms")

#fonction pour changer le nombre personne généré par la fonction suivante
def personne(event): 
    global nb_personnes
    nb_personnes = int(eval(entree1.get()))
    print("le nombre de personnes dans la foule aléatoire est: "+str(nb_personnes))
    
#permet de metre en démarrer/ relancer la simulation     
def go():
    "démarrage de l'animation"
    global compteur_etape
    compteur_etape=0
    global valeur_arret
    if valeur_arret ==0:
        valeur_arret =1    
    deplacement()
#permet de metre en pause/ arrêter la simulation     
def stop():
    "arrêt de l'animation"
    global valeur_arret    
    valeur_arret =0

#fonction qui crée une foule aléatoirement sur le canvas
def foule_aleatoire():
    i=0
    int(nb_personnes)
    dico_c[largeur_quadrillage-c,hauteur_quadrillage-2*c]=1
    while i<nb_personnes-1:
        r=random.randint(0,largeur_quadrillage/c-1)
        r1=random.randint(0,hauteur_quadrillage/c-1)
        if dico_c[r*c,r1*c]==0:
            dico_c[r*c,r1*c]=1
            i+=1
    go()

#fonction qui étudie les dépacement
def deplacement():
    global valeur_arret, vitesse
    for i in range(int(largeur_quadrillage/c)):
        a=i*c
        for j in range(int(hauteur_quadrillage/c)):
            b=j*c
            dico_voeux[a,b]=0 #On initialise les voeux de chaque case à 0 avant de commencer
    for x in range(int(largeur_quadrillage/c)):
        for y in range(int(hauteur_quadrillage/c)):#on parcourt les cases du tableau une par une 
#création des voeux
            a=abs(x-(x0/c))#distance entre la case et la sortie horizontalement
            b=abs(y-(y0/c)) #distance entre la case et la sortie verticalement 
            if dico_c[x*c,y*c]==2:
                dico_c[x*c,y*c]==2        
            if dico_c[x*c,y*c]==1: #On regarde les cases contenant une personne
                if y!=0 and y!=hauteur_quadrillage: #Si la case n'est ni sur la première ligne ni sur la dernière
                    if x==x0/c: #Si on est sur la même colonne que la sortie
                        if dico_c[x*c,(y-1)*c]==0: 
                            dico_voeux[x*c,y*c]=[x*c,(y-1)*c]  #Si il y a personne sur la case "au-dessus" la personne fait un voeux pour y aller
                        if dico_c[x*c,(y-1)*c]==2:
                            if dico_c[(x-1)*c,y*c]==0 and dico_c[(x+1)*c,y*c]==0:
                                r=random.randint(0,1)
                                if r==0:
                                    dico_voeux[x*c,y*c]=[(x-1)*c,y*c]
                                if r==1:
                                    dico_voeux[x*c,y*c]=[(x+1)*c,y*c]
                            if dico_c[(x-1)*c,(y)*c]==0 and dico_c[(x+1)*c,y*c]!=0:
                                dico_voeux[x*c,(y)*c]=[(x-1)*c,(y)*c]
                            if dico_c[(x-1)*c,(y)*c]!=0 and dico_c[(x+1)*c,y*c]==0:
                                dico_voeux[x*c,(y)*c]=[(x+1)*c,(y)*c]
                                
                    if a>=b and x<(x0/c): #Si la case est plus proche verticalement qu'horizontalement de la sortie and elle est "à gauche" de la sortie
                        if dico_c[(x+1)*c,y*c]==0:
                            dico_voeux[x*c,y*c]=[(x+1)*c,y*c]#Si la case à droite est vide on fait le voeux d'y aller
                        elif dico_c[x*c,(y-1)*c]==0:
                            dico_voeux[x*c,y*c]=[x*c,(y-1)*c]#Sinon on regarde si la case au-dessus est vide,si c'est le cas  on fait le voeux d'y aller
                        if dico_c[(x+1)*c,y*c]==2 and dico_c[x*c,(y-1)*c]==0:
                            dico_voeux[x*c,y*c]=[x*c,(y-1)*c]
                    elif a>=b and x>(x0/c) and x!=0: #Cas similaire au cas précédent mais la case est à droite
                        if dico_c[(x-1)*c,y*c]==0:
                            dico_voeux[x*c,y*c]=[(x-1)*c,y*c]
                        elif dico_c[x*c,(y-1)*c]==0:
                            dico_voeux[x*c,y*c]=[x*c,(y-1)*c]
                        if dico_c[(x-1)*c,y*c]==2 and dico_c[x*c,(y-1)*c]==0:
                            dico_voeux[x*c,y*c]=[x*c,(y-1)*c]
                    elif a<b: #Si la case est plus proche du milieu que du haut
                        if dico_c[x*c,(y-1)*c]==0:
                            dico_voeux[x*c,y*c]=[x*c,(y-1)*c]
                        elif dico_c[x*c,(y-1)*c]!=0:
                            if x<(x0/c):
                                if dico_c[(x+1)*c,y*c]==0:
                                    dico_voeux[x*c,y*c]=[(x+1)*c,y*c]
                            elif x>(x0/c):
                                if dico_c[(x-1)*c,y*c]==0:
                                    dico_voeux[x*c,y*c]=[(x-1)*c,y*c]

                            

                else:#cas où la personne se situe sur la ligne du haut(celle de la sortie)
                    if x<(x0/c):#à gauche de la sortie
                        if dico_c[(x+1)*c,y*c]==0:
                            dico_voeux[x*c,y*c]=[(x+1)*c,y*c]
                        if dico_c[(x+1)*c,y*c]==1:
                            dico_voeux[x*c,y*c]=[(x)*c,(y+1)*c]
                        if dico_c[(x+1)*c,y*c]==2 and dico_c[x*c,(y+1)*c]==0:
                            dico_voeux[x*c,y*c]=[(x)*c,(y+1)*c]
                    elif x>(x0/c):
                        if dico_c[(x-1)*c,y*c]==0:
                            dico_voeux[x*c,y*c]=[(x-1)*c,y*c]
                        if dico_c[(x-1)*c,y*c]==1:
                            dico_voeux[x*c,y*c]=[(x)*c,(y+1)*c]
                        if dico_c[(x-1)*c,y*c]==2 and dico_c[x*c,(y+1)*c]==0:
                            dico_voeux[x*c,y*c]=[(x)*c,(y+1)*c]
        

                
                
                    
                    
                        
#On a fait les voeux de chaque case et si elle souhaite allé à un endroit elle prend la valeur de la case en question
#On veut donc mettre en place le choix de la case qui va dans un certain endroit
    for x in range(int(largeur_quadrillage/c)):
        for y in range(int(hauteur_quadrillage/c)):#On parcourt toute les cases

            if dico_c[x*c,y*c]==0:#Si la case est vide en question est vide
                if y==(hauteur_quadrillage/c):#Si la case est sur la ligne du bas
                    if x!=0 and x!=(largeur_quadrillage/c):#Si on n'est pas sur la premiere ou la derniere ligne 
                        if x<x0/c and dico_voeux[(x-1)*c,y*c]==[x*c,y*c]:#Si on est a gauche de la sortie et que la case à gauche souhaite venir
                            dico_c[x*c,y*c]=1 #La case que l'on regarde devient noire(ie la personne se déplace dessus)
                            dico_c[(x-1)*c,y*c]=0#La case à gauche de celle que l'on regarde devient blache (ie la personne se part de cet endroit)
                        elif x>x0/c and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]: #Cas similaire Si on est a droite de la sortie et que la case à droite souhaite venir
                            dico_c[x*c,y*c]=1
                            dico_c[(x+1)*c,y*c]=0
                        if x==x0*c and dico_voeux[x*c,y*c]==[x*c,(y+1)*c]:#Si la case est sur la colonne de sortie                         
                            if dico_voeux[(x-1)*c,y*c]==[x*c,y*c] and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]: #Si les cases à gauche et a droites veulent venir
                                r=random.randint(0,2)#On met une probabilité de passage ou non des cases
                                if r==0:
                                    dico_c[x*c,y*c]=0
                                    dico_c[(x-1)*c,y*x]=1
                                    dico_c[(x+1)*c,y*x]=1
                                if r==1:
                                    dico_c[(x+1)*c,y*x]=0
                                    dico_c[x*c,y*c]=1
                                    dico_c[(x-1)*c,y*c]=1
                                elif r==2:
                                    dico_c[(x-1)*c,y*x]=0
                                    dico_c[x*c,y*c]=1
                                    dico_c[(x+1)*c,y*c]=1
                            elif dico_voeux[(x-1)*c,y*c]!=[x*c,y*c] and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]: #Si seul la case de droite veut venir elle va
                                r=random.randint(0,1)
                                if r==0:
                                    dico_c[(x+1)*c,y*c]=0
                                    dico_c[x*c,y*c]=1
                                    dico_c[x*c,(y+1)*c]=1
                                if r==1:
                                    dico_c[(x+1)*c,y*c]=1
                                    dico_c[x*c,y*c]=1
                                    dico_c[x*c,(y+1)*c]=0
                            elif dico_voeux[(x-1)*c,y*c]==[x*c,y*c] and dico_voeux[(x+1)*c,y*c]!=[x*c,y*c]: #Si seul la case de gauche veut venir elle va
                                r=random.randint(0,1)
                                if r==0:
                                    dico_c[(x-1)*c,y*c]=0
                                    dico_c[x*c,y*c]=1
                                    dico_c[x*c,(y+1)*c]=1
                                if r==1:
                                    dico_c[(x-1)*c,y*c]=1
                                    dico_c[x*c,y*c]=1
                                    dico_c[x*c,(y+1)*c]=0

                    
                if y<(hauteur_quadrillage/c)-1:#Si la case n'est pas sur la dernière ligne (le -1 est la car le for i in range nous donne que la derniere ligne est la "(hauteur_quadrillage/c)-1"
                    if x!=(largeur_quadrillage/c-1) and x!=0 :#Si la case est à la gauche de la sortie mais différentes des extremitées
                        if dico_voeux[(x-1)*c,y*c]==[x*c,y*c] and dico_voeux[x*c,(y+1)*c]==[x*c,y*c] and dico_voeux[(x+1)*c,(y)*c]==[x*c,y*c]:#Si la case en dessous et la case 
                            r=random.randint(0,2)
                            if r==0:
                                dico_c[(x+1)*c,y*c]=0
                                dico_c[x*c,y*c]=1
                            elif r==1:
                                dico_c[(x-1)*c,y*c]=0
                                dico_c[x*c,y*c]=1
                            elif r==2:
                                dico_c[x*c,(y+1)*c]=0
                                dico_c[x*c,y*c]=1
                        elif dico_voeux[(x-1)*c,y*c]==[x*c,y*c] and dico_voeux[x*c,(y+1)*c]!=[x*c,y*c] and dico_voeux[(x+1)*c,y*c]!=[x*c,y*c]:
                            dico_c[(x-1)*c,y*c]=0
                            dico_c[x*c,y*c]=1
                        elif dico_voeux[(x-1)*c,y*c]!=[x*c,y*c] and dico_voeux[x*c,(y+1)*c]==[x*c,y*c] and dico_voeux[(x+1)*c,y*c]!=[x*c,y*c]:
                            dico_c[x*c,(y+1)*c]=0
                            dico_c[x*c,y*c]=1
                        elif dico_voeux[(x-1)*c,y*c]!=[x*c,y*c] and dico_voeux[x*c,(y+1)*c]!=[x*c,y*c] and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]:
                            dico_c[(x+1)*c,y*c]=0
                            dico_c[x*c,y*c]=1
                        elif dico_voeux[(x-1)*c,y*c]==[x*c,y*c] and dico_voeux[x*c,(y+1)*c]==[x*c,y*c] and dico_voeux[(x+1)*c,y*c]!=[x*c,y*c]:
                            r=random.randint(0,1)
                            if r==0:
                                dico_c[(x-1)*c,y*c]=0
                                dico_c[x*c,y*c]=1
                            elif r==1:
                                dico_c[x*c,(y+1)*c]=0
                                dico_c[x*c,y*c]=1
                        elif dico_voeux[(x-1)*c,y*c]==[x*c,y*c] and dico_voeux[x*c,(y+1)*c]!=[x*c,y*c] and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]:
                            r=random.randint(0,1)
                            if r==0:
                                dico_c[(x-1)*c,y*c]=0
                                dico_c[x*c,y*c]=1
                            elif r==1:
                                dico_c[x*c,(x+1)*c]=0
                                dico_c[x*c,y*c]=1
                        elif dico_voeux[(x-1)*c,y*c]!=[x*c,y*c] and dico_voeux[x*c,(y+1)*c]==[x*c,y*c] and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]:
                            r=random.randint(0,1)
                            if r==1:
                                dico_c[(x+1)*c,y*c]=0
                                dico_c[x*c,y*c]=1
                            elif r==2:
                                dico_c[x*c,(y+1)*c]=0
                                dico_c[x*c,y*c]=1
                    if x==0:
                        if dico_voeux[x*c,(y+1)*c]==[x*c,y*c] and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]:
                            r=random.randint(0,1)
                            if r==0:
                                dico_c[x*c,y*c]=1
                                dico_c[(x+1)*c,y*c]=0
                                dico_c[x*c,(y+1)*c]=1
                            if r==1:
                                dico_c[x*c,y*c]=1
                                dico_c[(x+1)*c,y*c]=1
                                dico_c[x*c,(y+1)*c]=0                            
                        if dico_voeux[x*c,(y+1)*c]==[x*c,y*c]:
                            dico_c[x*c,y*c]=1
                            dico_c[x*c,(y+1)*c]=0
                        if dico_voeux[(x+1)*c,y*c]==[x*c,y*c]:
                            dico_c[x*c,y*c]=1
                            dico_c[(x+1)*c,y*c]=0
                    if x==(largeur_quadrillage/c-1):
                        if dico_voeux[x*c,(y+1)*c]==[x*c,y*c] and dico_voeux[(x-1)*c,y*c]==[x*c,y*c]:
                            r=random.randint(0,1)
                            if r==0:
                                dico_c[x*c,y*c]=1
                                dico_c[(x-1)*c,y*c]=0
                                dico_c[x*c,(y+1)*c]=1
                            if r==1:
                                dico_c[x*c,y*c]=1
                                dico_c[(x-1)*c,y*c]=1
                                dico_c[x*c,(y+1)*c]=0                            
                        if dico_voeux[x*c,(y+1)*c]==[x*c,y*c]:
                            dico_c[x*c,y*c]=1
                            dico_c[x*c,(y+1)*c]=0
                        if dico_voeux[(x-1)*c,y*c]==[x*c,y*c]:
                            dico_c[x*c,y*c]=1
                            dico_c[(x-1)*c,y*c]=0  
                                    
            
    redessiner()
    if valeur_arret>0:
        fen1.after(vitesse,deplacement) #Faire en sorte que la simulation avance tte seule                       

#fonction qui dessine le quadriallage d'apres les valeurs obtenue dans la fonction deplacement
def redessiner():
    global compteur_etape
    compteur_etape +=1
    compteur_cases=0
    can1.delete(ALL)
    damier()
    t=0
    while t!= largeur_quadrillage/c:
        u=0
        while u!= hauteur_quadrillage/c:
            x=t*c
            y=u*c
            if dico_c[x,y]==1:
                can1.create_rectangle(x, y, x+c, y+c, fill='black')
            elif dico_c[x,y]==0:
                can1.create_rectangle(x, y, x+c, y+c, fill='white')
            elif dico_c[x,y]==2:
                can1.create_rectangle(x, y, x+c, y+c, fill='red')
            u+=1
        t+=1
    dico_c[x0,y0]=0
    can1.create_rectangle(x0, y0, x0+c, y0+c, fill='blue')
    #La double boucle 'for' permet l'arrêt du code lorsqu'il n'y a plus personne dans la salle
    for x in range(int(largeur_quadrillage/c)):
        for y in range(int(hauteur_quadrillage/c)):
            if dico_c[x*c,y*c]!=1:
                compteur_cases +=1
    if compteur_cases==(largeur_quadrillage/c)*(hauteur_quadrillage/c):
        findefin=compteur_etape
        stop()
        L.append(compteur_etape/4)
        print("La foule évacue en "+str(compteur_etape)+"étape, soit "+str(compteur_etape/4)+"secondes pour "+str(nb_personnes)+" personnes")
                


#Initialisation des cellules On donne la valeur 0 à chaque cellule au debut du programme
for i in range(int((largeur_quadrillage)/c)): 
    for j in range(int((hauteur_quadrillage)/c)):
        x=i*c
        y=j*c
        dico_c[x,y]=0
        j+=1
    i+=1
    
    
fen1 = Tk()
can1 = Canvas(fen1, width =largeur_quadrillage, height =hauteur_quadrillage, bg ='white')
can1.bind("<Button-1>", click_gauche)
can1.bind("<Button-3>", click_droit)
can1.bind("<Button-2>", click_molette)
can1.pack(side =TOP, padx =5, pady =5)

damier()

b1 = Button(fen1, text ='Go!', command =go)
b2 = Button(fen1, text ='Stop', command =stop)
b1.pack(side =LEFT, padx =3, pady =3)
b2.pack(side =LEFT, padx =3, pady =3)
b3 = Button(fen1, text ='Foule Aléatoire', command =foule_aleatoire)
b3.pack(side =LEFT, padx =3, pady =3)

entree = Entry(fen1)
entree.bind("<Return>", change_vit)
entree.pack(side =RIGHT)
chaine = Label(fen1)
chaine.configure(text = "Attente entre chaque étape (ms) :")
chaine.pack(side =RIGHT)


entree1 = Entry(fen1)
entree1.bind("<Return>", personne)
entree1.pack(side =RIGHT)
chaine1 = Label(fen1)
chaine1.configure(text = "nombre de personne dans la piece:")
chaine1.pack(side =LEFT)

fen1.mainloop()

            from tkinter import *
import random
#Création des dictionnaires
dico_c={}
dico_voeux={}

#Liste qui permet les calculs de durée d'évacuation
L=[]

#initialise la variable qui compte les etape du programme                
compteur_etape=0

#Taille du quadriallage
largeur_quadrillage=600
hauteur_quadrillage=600

#dimensions d'une cellule
c=30

#On place la sortie
x0=300
y0=0
#initialise la variable qui gere la vitesse du programme     
vitesse=1

#Nombre de personne initilaement généré par la fonction qui crée cette foule
nb_personnes=10

#variable qui permet le fonctionnement de la fonction go()
valeur_arret=0


#fonction dessinant le tableau
def damier(): 
    ligne_vert()
    ligne_hor()
        
#crée les lignes verticales du quadriallage        
def ligne_vert():
    c_x = 0
    while c_x != largeur_quadrillage:
        can1.create_line(c_x,0,c_x,hauteur_quadrillage,width=1,fill='black')
        c_x+=c
        
#crée les lignes horizontales du quadriallage        
def ligne_hor():
    c_y = 0
    while c_y != hauteur_quadrillage:
        can1.create_line(0,c_y,largeur_quadrillage,c_y,width=1,fill='black')
        c_y+=c
        
#fonction rendant vivante la cellule cliquée donc met la valeur 1 pour la cellule cliquée au dico_case
def click_gauche(event): 
    x = event.x -(event.x%c)
    y = event.y -(event.y%c)
    can1.create_rectangle(x, y, x+c, y+c, fill='black')
    dico_c[x,y]=1

#fonction rendant vivante la cellule cliquée donc met la valeur 1 pour la cellule cliquée au dico_case    
def click_molette(event): 
    x = event.x -(event.x%c)
    y = event.y -(event.y%c)
    can1.create_rectangle(x, y, x+c, y+c, fill='red')
    dico_c[x,y]=2
    
#fonction tuant la cellule cliquée donc met la valeur 0 pour la cellule cliquée au dico_case
def click_droit(event): 
    x = event.x -(event.x%c)
    y = event.y -(event.y%c)
    can1.create_rectangle(x, y, x+c, y+c, fill='white')
    dico_c[x,y]=0
    
#fonction pour changer la vitesse(l'attente entre chaque étape)    
def change_vit(event):
    global vitesse
    vitesse = int(eval(entree.get())) # permet de modifier la valeur en tapant au clavier
    print("la vitesse est: "+str(vitesse)+"ms")

#fonction pour changer le nombre personne généré par la fonction suivante
def personne(event): 
    global nb_personnes
    nb_personnes = int(eval(entree1.get()))
    print("le nombre de personnes dans la foule aléatoire est: "+str(nb_personnes))
    
#permet de metre en démarrer/ relancer la simulation     
def go():
    "démarrage de l'animation"
    global compteur_etape
    compteur_etape=0
    global valeur_arret
    if valeur_arret ==0:
        valeur_arret =1    
    deplacement()
#permet de metre en pause/ arrêter la simulation     
def stop():
    "arrêt de l'animation"
    global valeur_arret    
    valeur_arret =0

#fonction qui crée une foule aléatoirement sur le canvas
def foule_aleatoire():
    i=0
    int(nb_personnes)
    dico_c[largeur_quadrillage-c,hauteur_quadrillage-2*c]=1
    while i<nb_personnes-1:
        r=random.randint(0,largeur_quadrillage/c-1)
        r1=random.randint(0,hauteur_quadrillage/c-1)
        if dico_c[r*c,r1*c]==0:
            dico_c[r*c,r1*c]=1
            i+=1
    go()

#fonction qui étudie les dépacement
def deplacement():
    global valeur_arret, vitesse
    for i in range(int(largeur_quadrillage/c)):
        a=i*c
        for j in range(int(hauteur_quadrillage/c)):
            b=j*c
            dico_voeux[a,b]=0 #On initialise les voeux de chaque case à 0 avant de commencer
    for x in range(int(largeur_quadrillage/c)):
        for y in range(int(hauteur_quadrillage/c)):#on parcourt les cases du tableau une par une 
#création des voeux
            a=abs(x-(x0/c))#distance entre la case et la sortie horizontalement
            b=abs(y-(y0/c)) #distance entre la case et la sortie verticalement 
            if dico_c[x*c,y*c]==2:
                dico_c[x*c,y*c]==2        
            if dico_c[x*c,y*c]==1: #On regarde les cases contenant une personne
                if y!=0 and y!=hauteur_quadrillage: #Si la case n'est ni sur la première ligne ni sur la dernière
                    if x==x0/c: #Si on est sur la même colonne que la sortie
                        if dico_c[x*c,(y-1)*c]==0: 
                            dico_voeux[x*c,y*c]=[x*c,(y-1)*c]  #Si il y a personne sur la case "au-dessus" la personne fait un voeux pour y aller
                        if dico_c[x*c,(y-1)*c]==2:
                            if dico_c[(x-1)*c,y*c]==0 and dico_c[(x+1)*c,y*c]==0:
                                r=random.randint(0,1)
                                if r==0:
                                    dico_voeux[x*c,y*c]=[(x-1)*c,y*c]
                                if r==1:
                                    dico_voeux[x*c,y*c]=[(x+1)*c,y*c]
                            if dico_c[(x-1)*c,(y)*c]==0 and dico_c[(x+1)*c,y*c]!=0:
                                dico_voeux[x*c,(y)*c]=[(x-1)*c,(y)*c]
                            if dico_c[(x-1)*c,(y)*c]!=0 and dico_c[(x+1)*c,y*c]==0:
                                dico_voeux[x*c,(y)*c]=[(x+1)*c,(y)*c]
                                
                    if a>=b and x<(x0/c): #Si la case est plus proche verticalement qu'horizontalement de la sortie and elle est "à gauche" de la sortie
                        if dico_c[(x+1)*c,y*c]==0:
                            dico_voeux[x*c,y*c]=[(x+1)*c,y*c]#Si la case à droite est vide on fait le voeux d'y aller
                        elif dico_c[x*c,(y-1)*c]==0:
                            dico_voeux[x*c,y*c]=[x*c,(y-1)*c]#Sinon on regarde si la case au-dessus est vide,si c'est le cas  on fait le voeux d'y aller
                        if dico_c[(x+1)*c,y*c]==2 and dico_c[x*c,(y-1)*c]==0:
                            dico_voeux[x*c,y*c]=[x*c,(y-1)*c]
                    elif a>=b and x>(x0/c) and x!=0: #Cas similaire au cas précédent mais la case est à droite
                        if dico_c[(x-1)*c,y*c]==0:
                            dico_voeux[x*c,y*c]=[(x-1)*c,y*c]
                        elif dico_c[x*c,(y-1)*c]==0:
                            dico_voeux[x*c,y*c]=[x*c,(y-1)*c]
                        if dico_c[(x-1)*c,y*c]==2 and dico_c[x*c,(y-1)*c]==0:
                            dico_voeux[x*c,y*c]=[x*c,(y-1)*c]
                    elif a<b: #Si la case est plus proche du milieu que du haut
                        if dico_c[x*c,(y-1)*c]==0:
                            dico_voeux[x*c,y*c]=[x*c,(y-1)*c]
                        elif dico_c[x*c,(y-1)*c]!=0:
                            if x<(x0/c):
                                if dico_c[(x+1)*c,y*c]==0:
                                    dico_voeux[x*c,y*c]=[(x+1)*c,y*c]
                            elif x>(x0/c):
                                if dico_c[(x-1)*c,y*c]==0:
                                    dico_voeux[x*c,y*c]=[(x-1)*c,y*c]

                            

                else:#cas où la personne se situe sur la ligne du haut(celle de la sortie)
                    if x<(x0/c):#à gauche de la sortie
                        if dico_c[(x+1)*c,y*c]==0:
                            dico_voeux[x*c,y*c]=[(x+1)*c,y*c]
                        if dico_c[(x+1)*c,y*c]==1:
                            dico_voeux[x*c,y*c]=[(x)*c,(y+1)*c]
                        if dico_c[(x+1)*c,y*c]==2 and dico_c[x*c,(y+1)*c]==0:
                            dico_voeux[x*c,y*c]=[(x)*c,(y+1)*c]
                    elif x>(x0/c):
                        if dico_c[(x-1)*c,y*c]==0:
                            dico_voeux[x*c,y*c]=[(x-1)*c,y*c]
                        if dico_c[(x-1)*c,y*c]==1:
                            dico_voeux[x*c,y*c]=[(x)*c,(y+1)*c]
                        if dico_c[(x-1)*c,y*c]==2 and dico_c[x*c,(y+1)*c]==0:
                            dico_voeux[x*c,y*c]=[(x)*c,(y+1)*c]
        

                
                
                    
                    
                        
#On a fait les voeux de chaque case et si elle souhaite allé à un endroit elle prend la valeur de la case en question
#On veut donc mettre en place le choix de la case qui va dans un certain endroit
    for x in range(int(largeur_quadrillage/c)):
        for y in range(int(hauteur_quadrillage/c)):#On parcourt toute les cases

            if dico_c[x*c,y*c]==0:#Si la case est vide en question est vide
                if y==(hauteur_quadrillage/c):#Si la case est sur la ligne du bas
                    if x!=0 and x!=(largeur_quadrillage/c):#Si on n'est pas sur la premiere ou la derniere ligne 
                        if x<x0/c and dico_voeux[(x-1)*c,y*c]==[x*c,y*c]:#Si on est a gauche de la sortie et que la case à gauche souhaite venir
                            dico_c[x*c,y*c]=1 #La case que l'on regarde devient noire(ie la personne se déplace dessus)
                            dico_c[(x-1)*c,y*c]=0#La case à gauche de celle que l'on regarde devient blache (ie la personne se part de cet endroit)
                        elif x>x0/c and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]: #Cas similaire Si on est a droite de la sortie et que la case à droite souhaite venir
                            dico_c[x*c,y*c]=1
                            dico_c[(x+1)*c,y*c]=0
                        if x==x0*c and dico_voeux[x*c,y*c]==[x*c,(y+1)*c]:#Si la case est sur la colonne de sortie                         
                            if dico_voeux[(x-1)*c,y*c]==[x*c,y*c] and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]: #Si les cases à gauche et a droites veulent venir
                                r=random.randint(0,2)#On met une probabilité de passage ou non des cases
                                if r==0:
                                    dico_c[x*c,y*c]=0
                                    dico_c[(x-1)*c,y*x]=1
                                    dico_c[(x+1)*c,y*x]=1
                                if r==1:
                                    dico_c[(x+1)*c,y*x]=0
                                    dico_c[x*c,y*c]=1
                                    dico_c[(x-1)*c,y*c]=1
                                elif r==2:
                                    dico_c[(x-1)*c,y*x]=0
                                    dico_c[x*c,y*c]=1
                                    dico_c[(x+1)*c,y*c]=1
                            elif dico_voeux[(x-1)*c,y*c]!=[x*c,y*c] and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]: #Si seul la case de droite veut venir elle va
                                r=random.randint(0,1)
                                if r==0:
                                    dico_c[(x+1)*c,y*c]=0
                                    dico_c[x*c,y*c]=1
                                    dico_c[x*c,(y+1)*c]=1
                                if r==1:
                                    dico_c[(x+1)*c,y*c]=1
                                    dico_c[x*c,y*c]=1
                                    dico_c[x*c,(y+1)*c]=0
                            elif dico_voeux[(x-1)*c,y*c]==[x*c,y*c] and dico_voeux[(x+1)*c,y*c]!=[x*c,y*c]: #Si seul la case de gauche veut venir elle va
                                r=random.randint(0,1)
                                if r==0:
                                    dico_c[(x-1)*c,y*c]=0
                                    dico_c[x*c,y*c]=1
                                    dico_c[x*c,(y+1)*c]=1
                                if r==1:
                                    dico_c[(x-1)*c,y*c]=1
                                    dico_c[x*c,y*c]=1
                                    dico_c[x*c,(y+1)*c]=0

                    
                if y<(hauteur_quadrillage/c)-1:#Si la case n'est pas sur la dernière ligne (le -1 est la car le for i in range nous donne que la derniere ligne est la "(hauteur_quadrillage/c)-1"
                    if x!=(largeur_quadrillage/c-1) and x!=0 :#Si la case est à la gauche de la sortie mais différentes des extremitées
                        if dico_voeux[(x-1)*c,y*c]==[x*c,y*c] and dico_voeux[x*c,(y+1)*c]==[x*c,y*c] and dico_voeux[(x+1)*c,(y)*c]==[x*c,y*c]:#Si la case en dessous et la case 
                            r=random.randint(0,2)
                            if r==0:
                                dico_c[(x+1)*c,y*c]=0
                                dico_c[x*c,y*c]=1
                            elif r==1:
                                dico_c[(x-1)*c,y*c]=0
                                dico_c[x*c,y*c]=1
                            elif r==2:
                                dico_c[x*c,(y+1)*c]=0
                                dico_c[x*c,y*c]=1
                        elif dico_voeux[(x-1)*c,y*c]==[x*c,y*c] and dico_voeux[x*c,(y+1)*c]!=[x*c,y*c] and dico_voeux[(x+1)*c,y*c]!=[x*c,y*c]:
                            dico_c[(x-1)*c,y*c]=0
                            dico_c[x*c,y*c]=1
                        elif dico_voeux[(x-1)*c,y*c]!=[x*c,y*c] and dico_voeux[x*c,(y+1)*c]==[x*c,y*c] and dico_voeux[(x+1)*c,y*c]!=[x*c,y*c]:
                            dico_c[x*c,(y+1)*c]=0
                            dico_c[x*c,y*c]=1
                        elif dico_voeux[(x-1)*c,y*c]!=[x*c,y*c] and dico_voeux[x*c,(y+1)*c]!=[x*c,y*c] and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]:
                            dico_c[(x+1)*c,y*c]=0
                            dico_c[x*c,y*c]=1
                        elif dico_voeux[(x-1)*c,y*c]==[x*c,y*c] and dico_voeux[x*c,(y+1)*c]==[x*c,y*c] and dico_voeux[(x+1)*c,y*c]!=[x*c,y*c]:
                            r=random.randint(0,1)
                            if r==0:
                                dico_c[(x-1)*c,y*c]=0
                                dico_c[x*c,y*c]=1
                            elif r==1:
                                dico_c[x*c,(y+1)*c]=0
                                dico_c[x*c,y*c]=1
                        elif dico_voeux[(x-1)*c,y*c]==[x*c,y*c] and dico_voeux[x*c,(y+1)*c]!=[x*c,y*c] and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]:
                            r=random.randint(0,1)
                            if r==0:
                                dico_c[(x-1)*c,y*c]=0
                                dico_c[x*c,y*c]=1
                            elif r==1:
                                dico_c[x*c,(x+1)*c]=0
                                dico_c[x*c,y*c]=1
                        elif dico_voeux[(x-1)*c,y*c]!=[x*c,y*c] and dico_voeux[x*c,(y+1)*c]==[x*c,y*c] and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]:
                            r=random.randint(0,1)
                            if r==1:
                                dico_c[(x+1)*c,y*c]=0
                                dico_c[x*c,y*c]=1
                            elif r==2:
                                dico_c[x*c,(y+1)*c]=0
                                dico_c[x*c,y*c]=1
                    if x==0:
                        if dico_voeux[x*c,(y+1)*c]==[x*c,y*c] and dico_voeux[(x+1)*c,y*c]==[x*c,y*c]:
                            r=random.randint(0,1)
                            if r==0:
                                dico_c[x*c,y*c]=1
                                dico_c[(x+1)*c,y*c]=0
                                dico_c[x*c,(y+1)*c]=1
                            if r==1:
                                dico_c[x*c,y*c]=1
                                dico_c[(x+1)*c,y*c]=1
                                dico_c[x*c,(y+1)*c]=0                            
                        if dico_voeux[x*c,(y+1)*c]==[x*c,y*c]:
                            dico_c[x*c,y*c]=1
                            dico_c[x*c,(y+1)*c]=0
                        if dico_voeux[(x+1)*c,y*c]==[x*c,y*c]:
                            dico_c[x*c,y*c]=1
                            dico_c[(x+1)*c,y*c]=0
                    if x==(largeur_quadrillage/c-1):
                        if dico_voeux[x*c,(y+1)*c]==[x*c,y*c] and dico_voeux[(x-1)*c,y*c]==[x*c,y*c]:
                            r=random.randint(0,1)
                            if r==0:
                                dico_c[x*c,y*c]=1
                                dico_c[(x-1)*c,y*c]=0
                                dico_c[x*c,(y+1)*c]=1
                            if r==1:
                                dico_c[x*c,y*c]=1
                                dico_c[(x-1)*c,y*c]=1
                                dico_c[x*c,(y+1)*c]=0                            
                        if dico_voeux[x*c,(y+1)*c]==[x*c,y*c]:
                            dico_c[x*c,y*c]=1
                            dico_c[x*c,(y+1)*c]=0
                        if dico_voeux[(x-1)*c,y*c]==[x*c,y*c]:
                            dico_c[x*c,y*c]=1
                            dico_c[(x-1)*c,y*c]=0  
                                    
            
    redessiner()
    if valeur_arret>0:
        fen1.after(vitesse,deplacement) #Faire en sorte que la simulation avance tte seule                       

#fonction qui dessine le quadriallage d'apres les valeurs obtenue dans la fonction deplacement
def redessiner():
    global compteur_etape
    compteur_etape +=1
    compteur_cases=0
    can1.delete(ALL)
    damier()
    t=0
    while t!= largeur_quadrillage/c:
        u=0
        while u!= hauteur_quadrillage/c:
            x=t*c
            y=u*c
            if dico_c[x,y]==1:
                can1.create_rectangle(x, y, x+c, y+c, fill='black')
            elif dico_c[x,y]==0:
                can1.create_rectangle(x, y, x+c, y+c, fill='white')
            elif dico_c[x,y]==2:
                can1.create_rectangle(x, y, x+c, y+c, fill='red')
            u+=1
        t+=1
    dico_c[x0,y0]=0
    can1.create_rectangle(x0, y0, x0+c, y0+c, fill='blue')
    #La double boucle 'for' permet l'arrêt du code lorsqu'il n'y a plus personne dans la salle
    for x in range(int(largeur_quadrillage/c)):
        for y in range(int(hauteur_quadrillage/c)):
            if dico_c[x*c,y*c]!=1:
                compteur_cases +=1
    if compteur_cases==(largeur_quadrillage/c)*(hauteur_quadrillage/c):
        findefin=compteur_etape
        stop()
        L.append(compteur_etape/4)
        print("La foule évacue en "+str(compteur_etape)+"étape, soit "+str(compteur_etape/4)+"secondes pour "+str(nb_personnes)+" personnes")
                


#Initialisation des cellules On donne la valeur 0 à chaque cellule au debut du programme
for i in range(int((largeur_quadrillage)/c)): 
    for j in range(int((hauteur_quadrillage)/c)):
        x=i*c
        y=j*c
        dico_c[x,y]=0
        j+=1
    i+=1
    
    
fen1 = Tk()
can1 = Canvas(fen1, width =largeur_quadrillage, height =hauteur_quadrillage, bg ='white')
can1.bind("<Button-1>", click_gauche)
can1.bind("<Button-3>", click_droit)
can1.bind("<Button-2>", click_molette)
can1.pack(side =TOP, padx =5, pady =5)

damier()

b1 = Button(fen1, text ='Go!', command =go)
b2 = Button(fen1, text ='Stop', command =stop)
b1.pack(side =LEFT, padx =3, pady =3)
b2.pack(side =LEFT, padx =3, pady =3)
b3 = Button(fen1, text ='Foule Aléatoire', command =foule_aleatoire)
b3.pack(side =LEFT, padx =3, pady =3)

entree = Entry(fen1)
entree.bind("<Return>", change_vit)
entree.pack(side =RIGHT)
chaine = Label(fen1)
chaine.configure(text = "Attente entre chaque étape (ms) :")
chaine.pack(side =RIGHT)


entree1 = Entry(fen1)
entree1.bind("<Return>", personne)
entree1.pack(side =RIGHT)
chaine1 = Label(fen1)
chaine1.configure(text = "nombre de personne dans la piece:")
chaine1.pack(side =LEFT)

fen1.mainloop()

            
