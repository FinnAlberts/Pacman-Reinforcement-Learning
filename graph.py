import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import time
import numpy as np
import pylab

figure, (axis1, axis2) = pyplot.subplots(2)

def graph():
    def animate(i):
        pull_data = open("rewards.txt", "r").read()
        data = pull_data.split('\n')
        x = []
        y = []
        z = []
        index = 0
        for line in data:
            if len(line) > 1:
                reward, score = line.split(' ')
                x.append(int(index))
                y.append(float(reward))
                z.append(float(score))
            index += 1
        axis1.clear()
        axis1.plot(x, y)
        axis1.set_title("Reward Progression")
        axis1.set_xlabel("Run")
        axis1.set_ylabel("Reward")

        axis2.plot(x, z)
        axis2.set_title("Score progression")
        axis2.set_xlabel("Run")
        axis2.set_ylabel("Score")


    animated = animation.FuncAnimation(figure, animate, interval=1000)


    plt.show()
    pyplot.show()


if __name__ == "__main__":
    graph()