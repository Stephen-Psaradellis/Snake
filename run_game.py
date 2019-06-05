import pygame, random, sys
from pygame.locals import *
import numpy as np
import random as rnd


def get_params(xs, ys, applepos):
    
    apple_up = ys[0] - applepos[1]
    apple_down = applepos[1] - ys[0] 
    apple_l = xs[0] - applepos[0]
    apple_r = applepos[0] - xs[0]
        
    snake_up = 0
    snake_down = 0
    snake_l = 0
    snake_r = 0
    
    
    ls = [ys[0]+1, 591 - ys[0], xs[0]+1, 591-xs[0],
          apple_up, apple_down, apple_l, apple_r,
          snake_up, snake_down, snake_l, snake_r]
    for i in range(len(ls)):
        if ls[i] ==0:
            pass
        elif ls[i] >0:
            ls[i] = 1-(ls[i]/590)
        else:
            ls[i] = (ls[i]/590)
    return np.array([ls])
    
    
    
def softmax(x):
    ex = np.exp(x)
    sum_ex = np.sum( np.exp(x))
    return ex/sum_ex
    
def sigmoid(x):
    return 1/(1+np.exp(-x))

def NN(entry, weights1, weights2):   
    layer1 = sigmoid(np.dot(entry, weights1))
    #output = softmax(sigmoid(np.dot(layer1, weights2)))
    output = softmax(layer1)
    return int(np.argmax(output))




def mutate(pop):
    if rnd.randrange(0,40) == 1:
        return True
    else:
        return False
    
def reproduce(xxx):
    #top 10% contrinutes 50% and the remaining 90% fill in the other 50%
    new_brains = []
    population = len(xxx)
    for repopulate in range(int(.50 *population)):
        options = (rnd.randrange(0,int(.1 *population)), rnd.randrange(0,int(.1 *population)))
        brain = options[0]
        weight_list = []
        for weights in range(len(xxx[brain])-1):
            c =  np.zeros(xxx[brain][weights].shape)
            for row in range(len(xxx[brain][weights])):
                for column in range(len(xxx[brain][weights][row])):
                    c[row,column] = xxx[options[rnd.randrange(0,2)]][weights][row,column]
                    if mutate(population) == True:
                        c[row,column] = np.random.rand(1)
            weight_list.append(c)
        weight_list.append(0)
        new_brains.append(weight_list)
    
    
    size = len(new_brains)
    for i in range(population - size):
        pick = rnd.randrange(int(.1 *population),len(xxx))
        xxx[pick][2] = 0
        new_brains.append(xxx[pick])
    return new_brains

def reproduce_v2(new_brains, xxx, stop):
    #each segment of 10% contributes slightly next to the next population
    population = len(xxx)
    for repopulate in range(int(.5 *population)):
        options = (rnd.randrange(0,int(.1 *population)), rnd.randrange(0,int(.1 *population)))
        brain = options[0]
        weight_list = []
        for weights in range(len(xxx[brain])-1):
            c =  np.zeros(xxx[brain][weights].shape)
            for row in range(len(xxx[brain][weights])):
                for column in range(len(xxx[brain][weights][row])):
                    c[row,column] = xxx[options[rnd.randrange(0,2)]][weights][row,column]
                    if mutate(stop) == True:
                        c[row,column] = c[row,column] + random.uniform(-.1, .1)
            weight_list.append(c)
        weight_list.append(0)
        new_brains.append(weight_list)
        if len(new_brains) == stop:
            return new_brains
    
    for i in range(int(.1*population)):
        xxx.pop(i)
  
    reproduce_v2(new_brains, xxx, stop)


def sort(alist):
    for index in range(1,len(alist)):
         currentvalue = alist[index]
         position = index
        
         while position>0 and alist[position-1][2] < currentvalue[2]:
             alist[position]=alist[position-1]
             position = position-1
        
         alist[position]=currentvalue    


def collide(x1, x2, y1, y2, w1, w2, h1, h2):
    if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:
        return True
    else:
        return False
    
def die(screen, score):
    f=pygame.font.SysFont('Arial', 30)
    t=f.render('Your score was: '+str(score), True, (0, 0, 0))
    screen.blit(t, (10, 270))
    pygame.display.update()
    pygame.time.wait(1000)
    pygame.display.quit()
    pygame.quit()
    return True

def run(first, second, generation):
    xs = [290, 290, 290, 290, 290]
    ys = [290, 280, 270, 260, 250]
    dirs = 0
    score = 0
    applepos = (random.randint(0, 59) * 10, random.randint(0, 59) * 10)
    pygame.init();
    s=pygame.display.set_mode((600, 600), DOUBLEBUF)
    s.set_alpha(None)
    pygame.display.set_caption('Snake')
    appleimage = pygame.Surface((10, 10))
    appleimage.fill((0, 255, 0))
    img = pygame.Surface((10, 10))
    img.fill((255, 0, 0))
    f = pygame.font.SysFont('Arial', 20)
    clock = pygame.time.Clock()
    dead = False
    pygame.time.delay(1000)
    
    timeout = 0
    while True:
        timeout += 1
        if timeout > 2500:
            die(s, score)
            break
        clock.tick(60)
        choice = NN(get_params(xs, ys, applepos), first, second)
        if choice == 0 and dirs != 0: #up
            dirs = 2
        elif choice == 1 and dirs != 2: #down
            dirs = 0
        elif choice == 2 and dirs != 1: #left
            dirs = 3
        elif choice == 3 and dirs != 3: #right
            dirs = 1
        i = len(xs)-1
        while i >= 2:
            if collide(xs[0], xs[i], ys[0], ys[i], 10, 10, 10, 10):
                dead = die(s, score)
            i-= 1
        if dead:
            break
        if collide(xs[0], applepos[0], ys[0], applepos[1], 10, 10, 10, 10):
            score+=1;
            xs.append(700)
            ys.append(700)
            applepos=(random.randint(0,59) * 10,random.randint(0,59) * 10)
        if xs[0] < 0 or xs[0] > 590 or ys[0] < 0 or ys[0] > 590:
            die(s, score)
            break
        i = len(xs)-1
        while i >= 1:
            xs[i] = xs[i-1]
            ys[i] = ys[i-1]
            i -= 1
        if dirs==0:
            ys[0] += 10
        elif dirs==1:
            xs[0] += 10
        elif dirs==2:
            ys[0] -= 10
        elif dirs==3:
            xs[0] -= 10 
        s.fill((255, 255, 255)) 
        for i in range(0, len(xs)):
            s.blit(img, (xs[i], ys[i]))
        s.blit(appleimage, applepos)
        s.blit(f.render("Score:" + str(score), True, (0, 0, 0)), (10, 10))
        s.blit(f.render("Generation: " + str(generation), True, (0, 0, 0)), (10, 30))
        pygame.display.update()
                                        
