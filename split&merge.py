# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 16:40:20 2017

@author: Administrator
"""

from PIL import Image #Importation de la librairie d'image PIL
im = Image.open("Image10.bmp") #Ouverture du fichier d'image
px = im.load() #Importation des pixels de l'image
from math import sqrt #Importation de la fonction sqrt de la librairie pxh
w,h=im.size #taille
from copy import deepcopy
#question 1
def pixel(x,y,px):
    r,g,b=px[x,y]
    return r,g,b

#qustion 2
def colorpixel(x,y,r,g,b,px):
    px[x,y] = int(r),int(g),int(b)
    return 0

#qustion 3
def colorregion(x0,y0,x1,y1,r,g,b,px):
    for i in range(y1-y0):
        for j in range(x1-x0):
            colorpixel(x0+j,y0+i,r,g,b,px)
    return 0

#question 4
import numpy as np
def color(x0,y0,x1,y1,px):
     r=np.zeros((x1-x0 , y1-y0))
     g=np.zeros((x1-x0 , y1-y0))
     b=np.zeros((x1-x0 , y1-y0))
     for i in range(y1-y0):
        for j in range(x1-x0):
            r[j,i]=px[j,i][0]
            g[j,i]=px[j,i][1]
            b[j,i]=px[j,i][2]
            
     return r,g,b        

r,g,b=color(0,0,w,h,px)     

def moyenne(x0,y0,x1,y1):    
    r_moyenne=np.mean(r[x0:x1,y0:y1]) 
    g_moyenne=np.mean(g[x0:x1,y0:y1]) 
    b_moyenne=np.mean(b[x0:x1,y0:y1]) 
    return r_moyenne ,g_moyenne ,b_moyenne

def ecart(x0,y0,x1,y1):
    r_ecart=sqrt(np.var(r[x0:x1,y0:y1])) 
    g_ecart=sqrt(np.var(g[x0:x1,y0:y1]))
    b_ecart=sqrt(np.var(b[x0:x1,y0:y1]))
    return (r_ecart+g_ecart+b_ecart)/3

def homogene(threshhold,x0,y0,x1,y1):
     if threshhold>ecart(x0,y0,x1,y1):
        return 1
     else:
        return 0
    
#question 5
def quadtree(threshhold,x0,y0,x1,y1):
    width=x1-x0
    long=y1-y0
    
    if width>1 and long>1:                
        if homogene(threshhold,x0,y0,x1,y1) == 1:
            r,g,b=moyenne(x0,y0,x1,y1)
            colorregion(x0,y0,x1,y1,r,g,b,px)
            L_regions.append((x0,y0,x1,y1,r,g,b))   #régions homogènes
        else:
            quadtree(threshhold,x0,y0,x0+int(width/2),y0+int(long/2))
            quadtree(threshhold,x0+int(width/2),y0+int(long/2),x1,y1) 
            quadtree(threshhold,x0+int(width/2),y0,x1,y0+int(long/2))
            quadtree(threshhold,x0,y0+int(long/2),x0+int(width/2),y1)
            
    else:
        r,g,b=pixel(x1,y1,px)
        colorregion(x0,y0,x1,y1,r,g,b,px)
        L_regions.append((x0,y0,x1,y1,r,g,b))   #régions homogènes
        
def homo(a, b, threshhold):
        r1=L_regions[a][4]
        g1=L_regions[a][5]
        b1=L_regions[a][6]
        r2=L_regions[b][4]
        g2=L_regions[b][5]
        b2=L_regions[b][6]
        t=sqrt((r2-r1)**2+(g2-g1)**2+(b2-b1)**2)
        if t<threshhold:
            return 1
        else:
            return 0
        
#teste si ces régions sont adjacentes
def neighbor(regions, i1, i2):
    if i1==i2:
        return 0
    else:
        x0=regions[i1][0]
        y0=regions[i1][1]
        x1=regions[i1][2]
        y1=regions[i1][3]
        x2=regions[i2][0]
        y2=regions[i2][1]
        x3=regions[i2][2]
        y3=regions[i2][3]
        
        w1=x1-x0
      
        h1=y1-y0
        
        w2=x3-x2
        
        h2=y3-y2
        
        center1=[(x0+x1)/2,(y0+y1)/2]
        center2=[(x2+x3)/2,(y2+y3)/2]
        
        
        if abs(center1[0]-center2[0])<(w1+w2)/2+1.25 and abs(center1[1]-center2[1])<(h1+h2)/2+1.25:
            return 1
        else:
            return 0
        
#construire une liste des regions de relation adjacante
def RAL(reg):
    number=len(reg)
    relation=[]
    for i in range(number):
        groupe=[]
        groupe.append(i)
        for j in range(number):
            if neighbor(reg, i, j)==1:
                groupe.append(j)
                #print('h')
        
        relation.append(groupe)
        
    return relation
        
def fusion(R,threshhold):
    no=[]
    yes=[]
    trait=[]
    longeur=len(R)
    for a in range(longeur):
        if a not in no:
            L=deepcopy(R)
            while True:
                l=rec(L,a,threshhold)
                l_copy=deepcopy(l)
                if l_copy==rec(L,a,threshhold):
                    no=list(set(no+l))
                    no.remove(a)
                    trait.append(l)
                    yes.append(a)
                    break                
    return trait
                       
def rec(Rela,origin,threshhold):
        if 'D' not in Rela[origin] and origin<=len(Rela):
            suppri=[]
            for j in Rela[origin][0:len(Rela[origin])]:
                 if j!=origin and 'D' not in Rela[j]:
                    if homo(origin, j, threshhold)==1:
                        Rela[origin]=list(set(Rela[origin]+Rela[j]))
                        Rela[j].append('D')
                    else:
                        suppri.append(j)

            Rela[origin]=list(set(Rela[origin])-set(suppri))
            return Rela[origin]


def merge(trai,regions):
    nb=len(trai)
    for i in range(nb):
           nombre=len(trai[i])
           if nombre>1:               
               r_tot=0
               g_tot=0
               b_tot=0
                          
               for l in trai[i]:
                   r_tot+=regions[l][4]
                   g_tot+=regions[l][5]
                   b_tot+=regions[l][6]
                   
               r_ave=r_tot/nombre
               g_ave=g_tot/nombre
               b_ave=b_tot/nombre
                
               for l in trai[i]:
                        x0=regions[l][0]
                        y0=regions[l][1]
                        x1=regions[l][2]
                        y1=regions[l][3]
                        colorregion(x0,y0,x1,y1,r_ave,g_ave,b_ave,px)

if __name__=="__main__":
    L_regions=[]
    quadtree(50 ,166 ,156 ,220,200)
    im.save('new.bmp')
    im.show( )
    print(len(L_regions))
    Relation=[]
    Relation=RAL(L_regions)
    tr=[]
    tr=fusion(Relation,100)
    merge(tr,L_regions)
    im.save('New.bmp')
    im.show( )
    print('end')