import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np
import pylab

fig, (ax1, ax2) = plt.subplots(2)

def animate(i):
    pull_data = open("rewards.txt", "r").read()
    data = pull_data.split('\n')
    x = []
    y = []
    z = []
    index = 0
    for line in data:
        if len(line) > 1:
            yar, zar = line.split(' ')
            x.append(int(index))
            y.append(float(yar))
            z.append(float(zar))
        index += 1
    ax1.clear()
    ax1.plot(x, y)
    ax1.set_title("Reward Progression")
    ax1.set_xlabel("Run")
    ax1.set_ylabel("Reward")

    ax2.plot(x, z)
    ax2.set_title("Score progression")
    ax2.set_xlabel("Run")
    ax2.set_ylabel("Score")


ani = animation.FuncAnimation(fig, animate, interval=1000)

mngr = plt.get_current_fig_manager()
# to put it into the upper left corner for example:
mngr.window.setGeometry(0,50, 640, 900)

plt.show()