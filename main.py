"""
Agent-based modeling of the spread of antibiotic resistance in a bacterial population,
taking into account spatial coordinates, reception of nutrients and antibacterial agents
"""

import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera


# function for initializing bacteria
def init_bacteria(n_bacterias, is_resistant):
    bacterias = [Bacteria(bac_coord=Coord(np.random.uniform(-200, 200), np.random.uniform(-200, 200)),
                          is_resistant=is_resistant)
                 for _ in range(n_bacterias)]
    return bacterias


# function for initializing the child cell
def init_newborn(parent_coord, is_resistant):
    newborn = Bacteria(bac_coord=parent_coord, is_resistant=is_resistant)
    return newborn


# function for initializing nutrition
def init_food(n_food):
    food = [Nutrition(coord=Coord(np.random.randint(-200, 200), np.random.randint(-200, 200))) for _ in range(n_food)]
    return food


# function for calculating the distance from bacteria to the nearest nutrient
def count_distance_for_food(bacteria_coord, nearest_food_coord):
    return np.sqrt((bacteria_coord.x - nearest_food_coord.x) ** 2 + (bacteria_coord.y - nearest_food_coord.y) ** 2)


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items()))

    cls.__str__ = __str__

    def __repr__(self):
        return self.__str__()

    cls.__repr__ = __repr__
    return cls


@auto_str
class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Coord) \
               and self.x == o.x \
               and self.y == o.y

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return hash((self.x, self.y))


@auto_str
class Bacteria:
    def __init__(self, bac_coord, age=0, is_resistant=False):
        self.bac_coord = bac_coord
        self.age = age
        self.is_resistant = False
        self.aimed_food_coord = None
        self.x_move_needed = 0
        self.y_move_needed = 0
        self.starving = 0
        self.speed = v_bac_sens
        self.division_time = division_time_sens

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Bacteria) \
               and self.bac_coord == o.bac_coord \
               and self.age == o.age and self.is_resistant == o.is_resistant \
               and self.aimed_food_coord == o.aimed_food_coord \
               and self.x_move_needed == o.x_move_needed \
               and self.y_move_needed == o.y_move_needed \
               and self.starving == o.starving \
               and self.speed == o.speed \
               and self.division_time == o.division_time

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return hash((self.coord, self.age, self.is_resistant, self.aimed_food_coord, self.x_move_needed,
                     self.y_move_needed, self.starving, self.speed, self.division_time))


@auto_str
class Nutrition:
    def __init__(self, coord):
        self.coord = coord

    def __eq__(self, o: object):
        return isinstance(o, Nutrition) and self.coord == o.coord

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return hash(self.coord)


n_bacterias = 200  # initial bacteria count

dict_color = {True: "red", False: "blue"}  # red - resistant, blue - sensitive

loss_probability = 0.2  # probability of accidental loss of plasmid
death_for_non_resistance_prob = 0.8  # probability of dying for a sensitive bacteria
capture_dist = 1  # plasmid capture distance
death_time = 50  # maximum bacteria lifetime
division_time_sens = 15  # division of sensitive cell
division_time_res = 25  # division of resistant cell
become_resistant_threshold = 0.99  # probability of a sensitive cell accidentally becoming resistant
hungry_death_time = 35  # the maximum time a bacterium lives without nutrition
v_bac_sens = 1  # movement speed of a sensitive bacteria to a nutrient
v_bac_res = 0.7  # movement speed of a resistant bacteria to a nutrient

antibiotic_time_1 = [i for i in range(50, 100)]  # time of the first entry of the antibiotic into the system
antibiotic_time_2 = [j for j in range(150, 200)]  # time of the second entry of the antibiotic into the system
antibiotic_time_3 = [k for k in range(250, 300)]  # time of the third entry of the antibiotic into the system
antibiotic_r = [r for r in range(0, 200, 4)]
r_num = 0

bacterias_list = init_bacteria(n_bacterias, is_resistant=False)  # initialization of bacteria
food = init_food(5000)  # initialization of nutrition

resist = []  # counting the number of resistant bacteria at each step
sensitive = []  # counting the number of sensitive bacteria at each step

fig = plt.figure()
ax = plt.axes()
camera = Camera(fig)

steps = 10  # simulation steps

for step in range(steps):
    # the appearance of bacteria and nutrient on the map
    ax.scatter(x=[i.bac_coord.x for i in bacterias_list], y=[j.bac_coord.y for j in bacterias_list],
               c=[dict_color[k.is_resistant] for k in bacterias_list], marker='o')
    ax.scatter(x=[i.coord.x for i in food], y=[j.coord.y for j in food], c="green",
               marker='o', s=10)

    # if it's time an enlarging antibiotic zone appears
    if (step in antibiotic_time_1) or (step in antibiotic_time_2) or (step in antibiotic_time_3):
        r = antibiotic_r[r_num]
        ax.add_artist(plt.Circle((0, 0), r, color="k", alpha=0.3))
        r_num += 1
    else:
        r_num = 0

    camera.snap()

    resist_sum = 0  # at each step we count how many bacteria with and without a plasmid, in order to build a graph
    for check in bacterias_list:
        if check.is_resistant:
            resist_sum += 1
    resist.append(resist_sum)
    sensitive.append(len(bacterias_list) - resist_sum)

    for bacteria in bacterias_list:

        bacteria.age += 1  # increasing the lifetime counter
        bacteria.starving += 1  # increasing the starving counter

        prob_for_become_res = np.random.random()
        if prob_for_become_res >= become_resistant_threshold:  # if value is greater than or equal to threshold
            bacteria.is_resistant = True  # sensitive bacteria becomes resistant
            bacteria.division_time = division_time_res
            bacteria.speed = v_bac_res

        if not bacteria.is_resistant:
            if bacteria.age % division_time_sens == 0:  # if it's time, the sensitive cell divides
                # the child cell appears at parent coordinates
                new_born_coords = Coord(bacteria.bac_coord.x, bacteria.bac_coord.y)
                new_born = init_newborn(new_born_coords, is_resistant=False)
                bacterias_list.append(new_born)

        else:
            if bacteria.age % division_time_res == 0:  # if it's time, the resistant cell divides
                prob_for_child = np.random.random()
                if prob_for_child <= loss_probability:  # if value is greater than or equal to threshold
                    plasmid_child = False  # resistant cell loses plasmid and becomes sensitive
                else:
                    plasmid_child = True  # or don't if value is lower

                # the child cell appears at parent coordinates
                new_born_coords = Coord(bacteria.bac_coord.x, bacteria.bac_coord.y)
                new_born = init_newborn(new_born_coords, is_resistant=plasmid_child)

                if new_born.is_resistant:
                    new_born.speed = v_bac_res
                    new_born.division_time = division_time_res
                bacterias_list.append(new_born)

        # if bacteria is too old or of it's starving long time
        if bacteria.age == death_time or bacteria.starving == hungry_death_time:
            bacterias_list.remove(bacteria)  # it dies and we remove it
            continue

        if not bacteria.is_resistant:
            for nearest_friend in bacterias_list:
                # if there is a resistant cell in capture distance
                if nearest_friend.is_resistant and np.sqrt((nearest_friend.bac_coord.x - bacteria.bac_coord.x) ** 2 + (
                        nearest_friend.bac_coord.y - bacteria.bac_coord.y) ** 2) <= capture_dist:
                    bacteria.is_resistant = True  # the bacterium acquires the plasmid
                    bacteria.division_time = division_time_res
                    bacteria.speed = v_bac_res

            # if sensitive bacteria is in range of antibiotic area it probably dies
            if (not bacteria.is_resistant) and ((step in antibiotic_time_1) or
                                                (step in antibiotic_time_2) or (step in antibiotic_time_3)):
                if (-r < bacteria.bac_coord.x) and (bacteria.bac_coord.x < r) and (-r < bacteria.bac_coord.y) \
                        and (bacteria.bac_coord.y < r):
                    prob_for_death = np.random.random()
                    if prob_for_death <= death_for_non_resistance_prob:
                        bacterias_list.remove(bacteria)
                        continue

        if len(food) == 0:  # if nutrition is over, then we don't do anything to find it
            continue

        if bacteria.starving > 5:  # if bacteria starving more than 5 steps, it looking for nutrition
            if bacteria.aimed_food_coord is None:  # if nearest food coordinates are not known, we find it
                nearest_food_distance = None
                nearest_food_idx = 0

                for idx, _food in enumerate(food):  # looking for nearest nutrition
                    distance_for_food = count_distance_for_food(bacteria.bac_coord, _food.coord)

                    if (nearest_food_distance is None) or (distance_for_food < nearest_food_distance):
                        nearest_food_distance = distance_for_food
                        nearest_food_idx = idx

                # write down the x and y of the nearest food
                aimed_food_coord_x = food[nearest_food_idx].coord.x
                aimed_food_coord_y = food[nearest_food_idx].coord.y
                new_aimed = Coord(aimed_food_coord_x, aimed_food_coord_y)
                bacteria.aimed_food_coord = new_aimed

                vector_x = bacteria.aimed_food_coord.x - bacteria.bac_coord.x
                vector_y = bacteria.aimed_food_coord.y - bacteria.bac_coord.y
                cos_a = vector_x / nearest_food_distance
                sin_a = vector_y / nearest_food_distance

                if not bacteria.is_resistant:  # for sensitive
                    # counting how much per unit of time it is necessary to shift in x and y to go to nutrient
                    bacteria.x_move_needed = v_bac_sens * cos_a
                    bacteria.y_move_needed = v_bac_sens * sin_a

                else:  # for resistant
                    # counting how much per unit of time it is necessary to shift in x and y to go to nutrient
                    bacteria.x_move_needed = v_bac_res * cos_a
                    bacteria.y_move_needed = v_bac_res * sin_a

            # if the nutrient has not been eaten, move towards it and try to eat it first
            if Nutrition(coord=bacteria.aimed_food_coord) in food:

                # movement itself - addition to the coordinates
                x_coord = bacteria.bac_coord.x + bacteria.x_move_needed
                y_coord = bacteria.bac_coord.y + bacteria.y_move_needed
                new_coords = Coord(x_coord, y_coord)
                bacteria.bac_coord = new_coords  # new coordinates of bacteria after movement

                if np.sqrt(
                        (bacteria.aimed_food_coord.x - bacteria.bac_coord.x) ** 2 +
                        (bacteria.aimed_food_coord.y - bacteria.bac_coord.y) ** 2
                ) <= (bacteria.speed / 2):  # if the distance is close enough
                    bacteria.starving = 0  # reset the starving time
                    food.remove(Nutrition(coord=bacteria.aimed_food_coord))  # remove eaten nutrient
                    bacteria.aimed_food_coord = None  # reset aimed nutrient info - looking for a new one

            else:  # if the nutrient has already been eaten, looking for a new one
                bacteria.aimed_food_coord = None

        else:  # if starving value is lower than 5, the bacteria does not need nutrition and moves randomly
            new_x_coord = bacteria.bac_coord.x + np.random.uniform(-2, 2)
            new_y_coord = bacteria.bac_coord.y + np.random.uniform(-2, 2)
            new_xy = Coord(new_x_coord, new_y_coord)
            bacteria.bac_coord = new_xy

    if step % 10 == 0:
        print('current step: {}'.format(step))

# model animation
animation = camera.animate()
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.show()
# animation.save('title.gif', writer='PillowWriter', fps=6)  # returns error, but saves gif file anyway
# plt.savefig(bbox_inches='tight')

# population over time plot
time = [i for i in range(steps)]
fig = plt.figure(figsize=(12, 8))
plt.plot(time, resist, c='red', label='Resistant strain', linewidth=7)
plt.plot(time, sensitive, c='blue', label='Sensitive strain', linewidth=7)
plt.xlabel("Simulation steps", fontsize=35)
plt.ylabel("Number of population", fontsize=35)
plt.legend(prop={'size': 45})
fig.suptitle('Bacteria population change over time', fontsize=35)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.grid()
plt.show()
plt.savefig("population_over_time.png")
