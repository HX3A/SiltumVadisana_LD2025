import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import integrate as sc

k = 1/1000
T_0 = 100
T_g = 20

# dt = 0.1 # s
t_max = 5000 # s


def SolveEiler(t, dt_inner = 0.1 ):
    # print(dt_inner)
    t_inner = t
    k_g = k
    T_gaisa = T_g

    def Tnew(T_old, k_k, dt_t, T_apk ):
        T_new = -k_k * (T_old - T_apk) * dt_t + T_old 
        return T_new
    
    T = np.zeros(shape=(len(t_inner) ,1))
    T[0] = T_0 # sakumnosac

    for index in range(1, len(T)):
        T[index ] = Tnew(T[index - 1], k_g, dt_inner, T_gaisa )
        # print(T[index])


    return t, T


# dt = 1500
# t = np.arange(0, t_max, dt) 
# plt.scatter(*SolveEiler(t, dt), label = dt)
dt = 1
t = np.arange(0, t_max, dt) 
plt.scatter(*SolveEiler(t, dt), label = dt)
dt = 0.1
t = np.arange(0, t_max, dt) 
plt.scatter(*SolveEiler(t, dt), label = dt)


def dTdx(t, temp, k, T_g):
    dTdt = -k *(temp - T_g)
    return dTdt

t = np.arange(0, t_max)
solution = sc.solve_ivp(dTdx, y0=[T_0, k, T_g], t_span=(0, t_max), args=[k, T_g], t_eval=t )
plt.plot(t,*solution.y, label = "Analitical")


plt.legend(loc = "upper right")
plt.xlabel("Time, s")
plt.ylabel("Temp, °C")

plt.show()