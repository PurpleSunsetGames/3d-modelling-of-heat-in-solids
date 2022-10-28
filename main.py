import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

'''
This program currently applies heat energy to a certain area of a cube and allows it to spread based on conductivity and
a basic lattice structure.

Soon, physics and optimizations will be added.
'''


fig = plt.figure()
ax = plt.axes(projection='3d')
x_l = 15
y_l = 15
z_l = 15
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
    if adding_ind - 1 < len(heatvals) and z_values[adding_ind - 1] < z:
        adjacent_point_heats.append(adding_ind - 1)

    if adding_ind + z_l < len(heatvals) and y_values[adding_ind + z_l] > y:
        adjacent_point_heats.append(adding_ind + z_l)
    if adding_ind - z_l < len(heatvals) and y_values[adding_ind - z_l] < y:
        adjacent_point_heats.append(adding_ind - z_l)

    if adding_ind + y_l * z_l < len(heatvals) and x_values[adding_ind + y_l * z_l] > x:
        adjacent_point_heats.append(adding_ind + y_l * z_l)
    if adding_ind - y_l * z_l < len(heatvals) and x_values[adding_ind - y_l * z_l] < x:
        adjacent_point_heats.append(adding_ind - y_l * z_l)
    indexes_adjacent.append(adjacent_point_heats)
    adding_ind += 1


def SigR(x):
    try:
        num = ((1/(1 + (math.e ** (1.6+(-.003 * x))))) - .5)*2
    except:
        num = 1
    if num > 1:
        num = .99
    if num < 0:
        num = 0.01
    return num


def SigB(x):
    try:
        num = ((1/(1 + (math.e ** (-2 + (.003 * x))))) - .5)*2
    except:
        num = 1
    if num > 1:
        num = .99
    if num < 0:
        num = 0.01
    return num


def SigG(x):
    try:
        num = ((1/(1 + (math.e ** (4 + (-.003 * x))))) - .5)*2
    except:
        num = 1
    if num > 1:
        num = 1
    if num < 0:
        num = 0
    return num


def on_click(event):
    print("clicked")


conductivity = 1
heat_amount = 35800


def update(i):
    colors = []
    index = 0
    prevheatvals = heatvals
    while index < len(z_values):
        x = x_values[index]
        y = y_values[index]
        z = z_values[index]
        if z == z_l - 1 and (y_l/2)-1 <= y <= (y_l/2)+1 and x > x_l-3 and i <= 5:
            heatvals[index] += heat_amount
        for item in indexes_adjacent[index]:
            prevheat = prevheatvals[index]
            if prevheatvals[item] > prevheat:
                difference = (prevheatvals[item] - prevheat)
                heatvals[index] += conductivity / 10 * difference
                heatvals[item] -= conductivity / 10 * difference
            elif prevheatvals[item] < prevheat:
                difference = (prevheat - prevheatvals[item])
                heatvals[index] -= conductivity / 10 * difference
                heatvals[item] += conductivity / 10 * difference
        colors.append((SigR(heatvals[index]), SigG(heatvals[index]), SigB(heatvals[index]), .7))
        x_values[index] += 0
        index += 1
    ax.clear()
    points = ax.scatter3D(x_values, y_values, z_values)
    points.set_facecolors(colors)
    print(f'ran frame {i} {len(z_values)}')

    #Comment the below line to disable saving the frames of the animation

    #plt.savefig(rf'C:\Users\tggt8\Videos\MatplotlibHeatStuff\{appendige}-{i}-d{x_l}-{y_l}-{z_l}-fig-heat-dispersion.png')

appendige = 'onespot1k'

fig.xlabel = 'x'
fig.ylabel = 'y'
fig.zlabel = 'z'
fig.canvas.mpl_connect('button_press_event', on_click)
a = FuncAnimation(fig=fig, func=update, interval=20)

#Writer = writers['ffmpeg']
#writer = Writer(fps=18, bitrate=1800)
print("Conductivity:", conductivity, '\nHeat being added:', heat_amount, '\nSize:', x_l, ' by ', y_l, ' by ', z_l, ' for ', x_l*y_l*z_l, ' total particles.')
plt.show()
