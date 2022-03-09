import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure(1)
ax1 = fig.add_subplot()
fig2 = plt.figure(2)
ax2 = fig2.add_subplot()


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
            x.append(float(index))
            y.append(float(yar))
            z.append(float(zar))
        index += 1
    ax1.clear()
    ax1.plot(x, y)
    ax2.plot(x, z)


ani = animation.FuncAnimation(fig, animate, interval=1000)
ani2 = animation.FuncAnimation(fig2, animate, interval=1000)
plt.show()
