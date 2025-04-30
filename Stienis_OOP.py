import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Simul():
    a : float 
    length :float #mm
    max_time : float #seconds
    nodes : int

    dx : float
    dt : float
    t_nodes : int 
    
    u : np.ndarray # temp array

    ut : np.ndarray

    time : np.ndarray 

    constant_temp : np.ndarray

    def __init__(self, alpha = 385 * 0.01, length = 50, max_time = 4, nodes = 100, constant_temp = np.array( [[0,200], [-1,200]] ), initTemp = 20):
        self.a = alpha
        self.length = length
        self.max_time = max_time
        self.nodes = nodes

        self.dx = length / (nodes-1)
        self.dt = 0.5 * self.dx**2 / self.a
        # self.dt = 0.05 # used for instability

        self.t_nodes = int(max_time/self.dt) + 1
        self.constant_temp = constant_temp

        self.time = np.arange(0, self.max_time, self.dt)
        self.ut = np.zeros(shape=(len(self.time), self.nodes))

        ### fill array
        # self.u = np.zeros(self.nodes) + 20
        self.SetInitTemp(initTemp)


        for i in range(0, len (constant_temp)):
            # print(len (constant_temp))
            # print(constant_temp[i,0])

            self.u[self.constant_temp[i,0]] = self.constant_temp[i][1]

    def SetInitTemp(self, initTemps):
        self.u = np.zeros(self.nodes) + initTemps
        

    def SetHeat(self):
        for i in range(0, len (self.constant_temp)):
            self.u[self.constant_temp[i,0]] = self.constant_temp[i][1]

    def PrintParams(self):
        print(self.dt)


    def Solve(self, constantHeat = True):

        for t in range(0, len(self.time)):
            w = self.u.copy()

            for i in range(1, self.nodes - 1):

                self.u[i] = self.dt * self.a * (w[i - 1] - 2 * w[i] + w[i + 1]) / self.dx ** 2 + w[i]

            if constantHeat or t < 10:
                self.SetHeat()

            self.ut[t] = np.array( self.u)

    def SolveNoInsul(self, constantHeat = True):

        for t in range(0, len(self.time)):
            w = self.u.copy()

            for i in range(1, self.nodes - 1):

                self.u[i] = self.dt * self.a * (w[i - 1] - 2 * w[i] + w[i + 1]) / self.dx ** 2 + w[i]

            self.u[0]  = self.dt * self.a * (- 2 * w[i] + w[i + 1]) / self.dx ** 2 + w[i]
            self.u[-1] = self.dt * self.a * (w[i - 1] - 2 * w[i]) / self.dx ** 2 + w[i]
            
            if constantHeat:
                self.SetHeat()


            self.ut[t] = np.array( self.u)

    def ReturnAsDF(self):
        return pd.DataFrame(self.u)
    

System = Simul()
# System = Simul( constant_temp = np.array( [[20,200]]), max_time=10 )

System = Simul( constant_temp = np.array( [[0,200], [-1, 0]]) )

### Solves with init conditions set as a sine wave with an amplitude 1000 degrees ###
x = np.arange(0, System.length + System.dx, System.dx)
sin_temp = 1000 * np.sin( 1.6 * np.pi * x / System.length  ) 
sin_temp = [x if x > 0 else 0 for x in sin_temp ]
System = Simul(max_time=100, constant_temp = np.array( []),initTemp= sin_temp)

# System.Solve(constantHeat=True)
System.SolveNoInsul(constantHeat=True)



fig, axis = plt.subplots()

pcm = axis.pcolormesh(System.ut,  cmap=plt.cm.turbo, vmin=0, vmax=200)
plt.colorbar(pcm)
axis.set_ylabel("Laiks, s")

axis.set_yticks([x for x in range(0, len(System.ut), int( len(System.ut) / 4))])
axis.set_yticklabels([f"{x * System.dt :.2f}" for x in range(0, len(System.ut), int( len(System.ut) / 4))])

axis.set_xlabel("Pozīcija, cm")
axis.set_xticks([x for x in range(0, System.nodes + 1, 10)])
axis.set_xticklabels([f"{x * System.dx :.1f}" for x in range(0, System.nodes + 1, 10)])


plt.show()
