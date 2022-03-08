import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):
    pull_data = open("rewards.txt", "r").read()
    data = pull_data.split('\n')
    x = []
    y = []
    index = 0
    for line in data:
        if len(line) > 1:
            x.append(float(index))
            y.append(float(line))
        index += 1
    ax1.clear()
    ax1.plot(x, y)


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
