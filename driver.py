import random
import numpy as np
import run_game



x, y, z = [],[], []



population_size = 1000
print('Population per generation: ' + str(population_size) + '\n')

ls_brains = []
for i in range(population_size):
    #FIX THIS
    ls_brains.append([np.random.rand(12,4), np.random.rand(4,4), 0])

for generation_count in range(100):
    for brain in ls_brains:
        
        dead = False
        xs = [290, 290, 290, 290, 290]
        ys = [290, 280, 270, 260, 250]
        dirs = 0
        score = 0
        applepos = (random.randint(0, 59) * 10, random.randint(0, 59) * 10)
        
        timeout = 0
        while True:
            timeout += 1
            if timeout > 2500:
                dead = True
                
            choice = run_game.NN(run_game.get_params(xs, ys, applepos), brain[0], brain[1])
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
                if run_game.collide(xs[0], xs[i], ys[0], ys[i], 10, 10, 10, 10):
                    dead = True
                i-= 1
            if dead:
                break
            if run_game.collide(xs[0], applepos[0], ys[0], applepos[1], 10, 10, 10, 10):
                score+=1;
                xs.append(700)
                ys.append(700)
                applepos=(random.randint(0,59) * 10,random.randint(0,59) * 10)
            if xs[0] < 0 or xs[0] > 590 or ys[0] < 0 or ys[0] > 590:
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
    
        brain[2] = score

    run_game.sort(ls_brains)
    print('Generation: ' + str(generation_count+1))
    total = []
    for i in range(len(ls_brains)):
        total.append(ls_brains[i][2])
    print('Mean Score: ' + str(np.mean(total)))
    max = ls_brains[0][2]
    print('Max Score: ' + str(max))
    print()
    run_game.run(ls_brains[0][0], ls_brains[0][1], generation_count+1)
    new = []
    run_game.reproduce_v2(new, ls_brains, len(ls_brains))                                            
    ls_brains = new                                       
                            
    
    x.append(generation_count +  1)
    y.append(np.mean(total))
    z.append(max)
    
import matplotlib.pyplot as plt
plt.plot(x, y, '-r')
plt.plot(x, z, '-b')
plt.show()

'''
things to fix/improve/finish

sorting algorithm faster
check computer vision, snake should see fi its gonna hit itself
reproduction parameters, what is best(ie mutation rate, survival rate)

those who score better should reproduce more



'''















































