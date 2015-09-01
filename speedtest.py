import numpy as np
import random as rnd
#import math
class Individual:
    def __init__(self):
        pass
    def func1(self):    
        np.random.randint(0,10)
    def func2(self):
        rnd.randint(0,10)


class Simulation:
    def __init__(self):
        self.freddy=Individual()
        self.maxtime=1000000
    def run(self):
        for x in xrange(self.maxtime):
            self.freddy.func1()
            #self.freddy.func2()
        
if __name__ == '__main__':                
    simulation=Simulation()
    import cProfile
    cProfile.run('simulation.run()')                  