import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from numba import njit, prange, jit
import math

'''
This program currently applies heat energy to a certain area of a cube and allows it to spread based on conductivity and
a basic lattice structure.

Soon, physics and optimizations will be added.
'''


fig = plt.figure()
ax = plt.axes(projection='3d')
x_l = 40
y_l = 40
z_l = 40
x_values, y_values, z_values, heatvals = [], [], [], []
indexes_adjacent = []
x_curr = 0
y_curr = 0
z_curr = 0

while x_curr < x_l:
    y_curr = 0
    while y_curr < y_l:
        z_curr = 0
        while z_curr < z_l:
            z_values.append(z_curr)
            y_values.append(y_curr)
            x_values.append(x_curr)
            heatvals.append(0)
            z_curr += 1
        y_curr += 1
    x_curr += 1

adding_ind = 0
while adding_ind < len(z_values):
    adjacent_point_heats = []
    z = z_values[adding_ind]
    y = y_values[adding_ind]
    x = x_values[adding_ind]
    if adding_ind + 1 < len(heatvals) and z_values[adding_ind + 1] > z:
        adjacent_point_heats.append(adding_ind + 1)
    else:
        adjacent_point_heats.append(-1)
    if adding_ind - 1 < len(heatvals) and z_values[adding_ind - 1] < z:
        adjacent_point_heats.append(adding_ind - 1)
    else:
        adjacent_point_heats.append(-1)

    if adding_ind + z_l < len(heatvals) and y_values[adding_ind + z_l] > y:
        adjacent_point_heats.append(adding_ind + z_l)
    else:
        adjacent_point_heats.append(-1)
    if adding_ind - z_l < len(heatvals) and y_values[adding_ind - z_l] < y:
        adjacent_point_heats.append(adding_ind - z_l)
    else:
        adjacent_point_heats.append(-1)

    if adding_ind + y_l * z_l < len(heatvals) and x_values[adding_ind + y_l * z_l] > x:
        adjacent_point_heats.append(adding_ind + y_l * z_l)
    else:
        adjacent_point_heats.append(-1)
    if adding_ind - y_l * z_l < len(heatvals) and x_values[adding_ind - y_l * z_l] < x:
        adjacent_point_heats.append(adding_ind - y_l * z_l)
    else:
        adjacent_point_heats.append(-1)
    indexes_adjacent.append(adjacent_point_heats)
    adding_ind += 1


def on_click(event):
    print("clicked")


conductivity = .7
heat_amount = 8800


def update(i):
    global heatvals, x_values, y_values, z_values
    colors = np.zeros((len(z_values), 4))
    heatvals, x_values, y_values, z_values, colors = update_njit(np.array(heatvals), np.array(x_values),
                                                                 np.array(y_values), np.array(z_values),
                                                                 np.array(indexes_adjacent), colors,
                                                                 np.array(heatvals), i, len(z_values))
    print(len(colors))
    print(x_values.dtype, x_values.shape)
    ax.clear()
    points = ax.scatter3D(x_values, y_values, z_values)
    points.set_facecolors(colors)
    del colors
    print(f'ran frame {i} with {len(z_values)} res')

    #Comment the below line to disable saving the frames of the animation
    plt.savefig(rf'{appendige}-{i}-d{x_l}-{y_l}-{z_l}-fig-heat-dispersion.png')


@jit(parallel=True)
def update_njit(heatvals_list, x_values_list, y_values_list, z_values_list, ind_adjacent_list, colors, prevheatvals, i, l):
    for inde in prange(l):
        x = x_values_list[inde]
        y = y_values_list[inde]
        z = z_values_list[inde]
        if z == z_l - 1 and (y_l / 2) - 1 <= y <= (y_l / 2) + 1 and x > x_l - 3 and i <= 5:
            heatvals_list[inde] += heat_amount
        for item in ind_adjacent_list[inde]:
            if item != -1:
                prevheat = prevheatvals[inde]
                if prevheatvals[item] > prevheat:
                    difference = (prevheatvals[item] - prevheat)
                    heatvals_list[inde] += conductivity / 10 * difference
                    heatvals_list[item] -= conductivity / 10 * difference
                elif prevheatvals[item] < prevheat:
                    difference = (prevheat - prevheatvals[item])
                    heatvals_list[inde] -= conductivity / 10 * difference
                    heatvals_list[item] += conductivity / 10 * difference
        colors[inde] = [Sig(heatvals_list[inde], 0, -.003), Sig(heatvals_list[inde], 1, -.002), Sig(heatvals_list[inde], 1.5, -.001), .9]
        x_values_list[inde] += 0
    return heatvals_list, x_values_list, y_values_list, z_values_list, colors


@njit
def Sig(x, of, m):
    try:
        num = ((1 / (1 + (math.e ** (of + (m * x))))) - .5) * 2
    except:
        num = 1
    if num > 1:
        num = .99
    if num < 0:
        num = 0.01
    return num


appendige = 'onespot'

fig.xlabel = 'x'
fig.ylabel = 'y'
fig.zlabel = 'z'
fig.canvas.mpl_connect('button_press_event', on_click)
a = FuncAnimation(fig=fig, func=update, interval=20)

#Writer = writers['ffmpeg']
#writer = Writer(fps=18, bitrate=1800)
print("Conductivity:", conductivity, '\nHeat being added:', heat_amount, '\nSize:', x_l, ' by ', y_l, ' by ', z_l, ' for ', x_l*y_l*z_l, ' total particles.')
plt.show()
