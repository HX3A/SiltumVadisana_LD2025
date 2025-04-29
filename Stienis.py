import numpy as np
import matplotlib.pyplot as plt

a = 385 * 0.01
length = 50 
time = 4 #seconds
nodes = 100

dx = length / (nodes-1)
dt = 0.5 * dx**2 / a
# dt = 0.01
t_nodes = int(time/dt) + 1

u = np.zeros(nodes) + 20 # Sakuma temp

# Boundary
u[0] = 200
u[-1] = 0

fig, axis = plt.subplots()

pcm = axis.pcolormesh([u], cmap=plt.cm.jet, vmin=0, vmax=200)
plt.colorbar(pcm, ax=axis)
axis.set_ylim([-2, 3])

counter = 0

while counter < time :

    w = u.copy()

    for i in range(1, nodes - 1):

        u[i] = dt * a * (w[i - 1] - 2 * w[i] + w[i + 1]) / dx ** 2 + w[i]

    counter += dt

    print("t: {:.3f} [s], Average temperature: {:.2f} Celcius".format(counter, np.average(u)))

    pcm.set_array([u])
    axis.set_title("Distribution at t: {:.3f} [s].".format(counter))
    plt.pause(0.01)


plt.show()
