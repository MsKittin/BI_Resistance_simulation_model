import numpy as np
import matplotlib.pyplot as plt
import math
from celluloid import Camera


bacterials_num = 50
bacterias = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(bacterials_num)]

'''
0 - икс бактерии
1 - игрек бактерии
2 - время жизни
3 - наличие плазмиды
4 - координата ближайшей еды по х
5 - координаты ближайшей еды по у
6 - сколько надо за шаг сместится по х к ближайшей еде
7 - сколько надо за шаг сместится по у к ближайшей еде
8 - время сколько бактерия живет без еды'''

for bacteria in bacterias:
    bacteria[0] += np.random.uniform(-20, 20)
    bacteria[1] += np.random.uniform(-20, 20)
    bacteria[3] = np.random.choice([0, 1])

food = [[np.random.randint(-20, 20), np.random.randint(-20, 20)] for i in range(200)]

dict_color = {1: "red", 0: "blue"}
loss_probability = 0.05  # вероятность потерять плазмиду
death_for_non_resistance_prob = 0.8  # вероятность умереть не резистетной бактерии
capture_dist = 1  # расстояние захвата плазмиды
death_time = 50  # время через которое клетка умрет от старости
hungry_death_time = 10  # умрет от голода
division_time = 15  # поделится
v_bac = 0.5  # скорость бактерии движения к еде


fig = plt.figure()
ax = plt.axes()
camera = Camera(fig)


for step in range(100):
    ax.scatter(x=[i[0] for i in bacterias], y=[j[1] for j in bacterias], c=[dict_color[k[3]] for k in bacterias],
               marker='o', s=50)
    ax.scatter(x=[i[0] for i in food], y=[j[1] for j in food], c="green",
               marker='o', s=10)
    camera.snap()
    for bacteria in bacterias:
        bacteria[2] += 1  # время просто жизни
        bacteria[8] += 1  # сколько голодаем
        if bacteria[2] % division_time == 0:  # делимся если пришло время. Можем потерять плазмиду
            if bacteria[3] == 1:
                prob_for_son = np.random.random()
                if prob_for_son <= loss_probability:
                    plasm_son = 0
                else:
                    plasm_son = 1
            else:
                plasm_son = 0
            bacterias.append([bacteria[0], bacteria[1], 0, plasm_son, 0, 0, 0, 0, 0])
        if bacteria[2] == death_time or bacteria[8] == hungry_death_time:  # дохнем от старости или голода
            bacterias.remove(bacteria)
        if bacteria[3] == 0:  # приобретаем плазмиду если есть че рядом
            for nearest_friend in bacterias:
                if nearest_friend[3] == 1 and math.sqrt((nearest_friend[0] - bacteria[0]) ** 2 + (nearest_friend[1] - bacteria[1]) ** 2) <= capture_dist:
                    bacteria[3] = 1
            if bacteria[3] == 0:
                prob_for_death = np.random.random()
                if prob_for_death <= death_for_non_resistance_prob:
                    bacterias.remove(bacteria)
        if bacteria[4] == bacteria[5] == 0:  # координаты еды неизвестны если - то ищем ближайшую еду.
            where_to_go = []
            for nearest_food in food:  # идем по массиву еды ищем ближайшую
                dist_for_food = math.sqrt((bacteria[0] - nearest_food[0]) ** 2 + (bacteria[1] - nearest_food[1]) ** 2)
                where_to_go.append(dist_for_food)
            bacteria[4] = food[where_to_go.index(min(where_to_go))][0]  # записываем где по икс и игрек ближайшая еда
            bacteria[5] = food[where_to_go.index(min(where_to_go))][1]
            vector_x = bacteria[4] - bacteria[0]
            vector_y = bacteria[5] - bacteria[1]
            cos_a = vector_x / min(where_to_go)
            sin_a = vector_y / min(where_to_go)
            bacteria[6] = v_bac * cos_a  # считаем сколько за единицу времени надо сместиться по х и у чтобы идти к еде
            bacteria[7] = v_bac * sin_a
        if [bacteria[4], bacteria[5]] in food:  # если еду не съели - движемся к ней и пытаемся съесть первыми
            bacteria[0] += bacteria[6]  # собственно движение - прибавление к координате
            bacteria[1] += bacteria[7]
            if math.sqrt((bacteria[4] - bacteria[0]) ** 2 + (bacteria[5] - bacteria[1]) ** 2) <= (v_bac / 2):  # если расстояние достаточно близкое
                bacteria[8] = 0  # обнуляем время голода
                food.remove([bacteria[4], bacteria[5]])  # удаляем еду
                bacteria[4] = 0  # обнуляем инфу о еде - ишем новую
                bacteria[5] = 0
        else:  # если еду уже съели - ищем новую
            bacteria[4] = 0
            bacteria[5] = 0
    print(step)


animation = camera.animate()
plt.show()
plt.savefig()