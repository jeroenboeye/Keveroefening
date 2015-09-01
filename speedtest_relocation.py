import numpy as np
import random
import math
class Individual:
    def __init__(self):
        self.x=0
        self.y=0
        self.dispersal_kernel=[12,3,0.5,0.4,9,1,1,5,0.5,-1]
        self.nr_kernel_steps=len(self.dispersal_kernel) 
        self.distance=0
        self.max_angle=2*math.pi
        self.mutation_rate=0.005
        
    def relocate(self):    
        total_kernel_prob=0
        for d in self.dispersal_kernel: #sum all the positive kernel values (negative = 0)
            if d>0:
                total_kernel_prob+=d      
        if total_kernel_prob>0:         #if not all kernel values are negative we calculate a distance
            proportional_kernel=self.dispersal_kernel[:]
            for d in xrange(self.nr_kernel_steps):
                if proportional_kernel[d]<0: proportional_kernel[d]=0   #change negative values into zeros         
            for x in xrange(self.nr_kernel_steps-1):
                proportional_kernel[x+1]=proportional_kernel[x]+proportional_kernel[x+1] #make the kernel cummulative            
            samplenr=random.uniform(0,total_kernel_prob)
            if proportional_kernel[0]>samplenr:#sample distance using random nr 
                distance=0
            else:
                for x in xrange(self.nr_kernel_steps-1):
                    if proportional_kernel[x] <= samplenr < proportional_kernel[x+1]:
                        distance=x+1
                        break   
        else: 
            distance=0
        self.distance=distance    
        if distance>0:
            angle=random.uniform(0,self.max_angle)  
            x_vector=distance*math.cos(angle)
            y_vector=distance*math.sin(angle)
            self.x=int(round(x_vector))+self.nr_kernel_steps-1
            self.y=int(round(y_vector))+self.nr_kernel_steps-1 
            
    def mutating(self,old_kernel,time_ratio):
        #minimum=-10 #minimum value to prevent too much drifting in neutral selective space
        random.randint(0,5-1)
        '''        
        self.time_ratio=time_ratio
        new_kernel=old_kernel[:]
        for n in xrange(self.nr_kernel_steps):
            if random.random() < self.mutation_rate: # mutation or not     
                mut_sd  = 2 * math.exp(-5*self.time_ratio)
                #mut_sd=2
                mutation=np.random.normal(0,0.1+mut_sd) 
                new_kernel[n] += mutation              
        return new_kernel
        '''    


class Simulation:
    def __init__(self):
        self.freddy=Individual()
        self.maxtime=300000
        self.dispersal_kernel=[12,3,0.5,0.4,9,1,1,5,0.5,-1]
    def run(self):
        for x in xrange(self.maxtime):
            self.freddy.relocate()
            #self.freddy.mutating(self.dispersal_kernel,x/float(self.maxtime))
        
if __name__ == '__main__':                
    simulation=Simulation()
    import cProfile
    cProfile.run('simulation.run()')                  