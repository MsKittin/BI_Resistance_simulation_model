import numpy as np
import matplotlib.pyplot as plt
import math
from celluloid import Camera

bacterias = [[0, 0, 0, 0] for i in range(50)]
for bacteria in bacterias:
    bacteria[0] += np.random.uniform(-5, 5)
    bacteria[1] += np.random.uniform(-5, 5)
    bacteria[3] = np.random.choice([0, 1])

dict_color = {1: "red", 0: "blue"}
loss_probability = 0.05
death_for_non_resistance_prob = 0.9
capture_dist = 1
death_time = 15
division_time = 5

fig = plt.figure()
ax = plt.axes()
camera = Camera(fig)

for step in range(50):
    ax.scatter(x=[i[0] for i in bacterias], y=[j[1] for j in bacterias], c=[dict_color[k[3]] for k in bacterias],
               marker='o')
    camera.snap()
    for bacteria in bacterias:
        bacteria[2] += 1
        if bacteria[2] % division_time == 0:
            if bacteria[3] == 1:
                prob_for_son = np.random.random()
                if prob_for_son <= loss_probability:
                    plasm_son = 0
                else:
                    plasm_son = 1
            else:
                plasm_son = 0
            bacterias.append([bacteria[0], bacteria[1], 0, plasm_son])
        if bacteria[2] == death_time:
            bacterias.remove(bacteria)
        if bacteria[3] == 0:
            for nearest_friend in bacterias:
                if nearest_friend[3] == 1 and math.sqrt((nearest_friend[0] - bacteria[0]) ** 2 + (nearest_friend[1] - bacteria[1]) ** 2) <= capture_dist:
                    bacteria[3] = 1
            if bacteria[3] == 0:
                prob_for_death = np.random.random()
                if prob_for_death <= death_for_non_resistance_prob:
                    bacterias.remove(bacteria)
        bacteria[0] += np.random.uniform(-2, 2)
        bacteria[1] += np.random.uniform(-2, 2)
        print(step)

animation = camera.animate()
plt.show()
animation.save('bacterias.gif', writer='PillowWriter', fps=2)