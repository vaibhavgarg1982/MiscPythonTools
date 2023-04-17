from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import math
import collections
import time

# initializing a figure in  which the graph will be plotted
fig = plt.figure()


# marking the x-axis and y-axis
axis = plt.axes(xlim=(-4, 10), ylim=(-2, 2))

lines = []
for index in range(20):
    lobj = axis.plot([], [], lw=0.3)[0]
    lines.append(lobj)
angles = [math.radians(ang) for ang in range(0, 360)]
xdata, ydata = [], []
xdata = collections.deque(maxlen=360)
ydata = collections.deque(maxlen=360)
closedY = collections.deque(maxlen=360)
closedX = collections.deque(maxlen=360)


def init():
    for ln in lines:
        ln.set_data([], [])
    return lines


def animate(i, *fargs):
    # start = time.time()
    xs = []
    ys = []
    # draws a circle
    y = [math.sin(ang) for ang in angles]
    x = [math.cos(ang) for ang in angles]

    xs.append(x)
    ys.append(y)
    lines[0].set_data(x, y)
    index = 0
    phases = fargs[0::2]  # every alternate value is the phase
    hmag = fargs[1::2]

    for index, phase in enumerate(
        phases,
        start=1,
    ):
        xs.append(
            [
                xs[index - 1][i]
                + (hmag[index - 1]) * math.cos((index + 1) * ang + phase)
                for ang in angles
            ]
        )
        ys.append(
            [
                ys[index - 1][i]
                + (hmag[index - 1]) * math.sin((index + 1) * ang + phase)
                for ang in angles
            ]
        )
        lines[index].set_data(xs[-1], ys[-1])
        pass  # tempx  =

    # actual curve drawn in this line
    ydata.append(ys[-1][i])
    # connection to the last epicircle to the curve
    x_connect = [xs[-1][i], 3.5 + angles[len(ydata) - 1]]
    y_connect = [ys[-1][i], ydata[-1]]

    closedY.append(ys[-1][i])
    closedX.append(xs[-1][i])

    lines[-3].set_data([x + 3.5 for x in angles[0 : len(ydata)]], ydata)
    lines[-3].set_linewidth(1.5)
    lines[-2].set_data(x_connect, y_connect)
    lines[-2].set_linewidth(0.8)
    lines[-1].set_data(closedX, closedY)
    lines[-1].set_color("black")
    lines[-1].set_linewidth(2)
    # print(time.time()-start)

    return lines


# fargs pairs of phase and magnitude, starting at 2nd harmonic.
fargs = [
    0,
    0,
    0,
    1 / 3,
    0,
    0,
    0,
    1 / 5,
    0,
    0,
    0,
    1 / 7,
    0,
    0,
    0,
    1 / 9,
    0,
    0,
    0,
    1 / 11,
    0,
    0,
    0,
    1 / 13,
    0,
    0,
    0,
    1 / 15,
    0,
    0,
    0,
    1 / 17,
    0,
    0,
    0,
    1 / 19,
]
# fargs = list(np.random.random(24))
anim = FuncAnimation(
    fig,
    animate,
    fargs=fargs,
    init_func=init,
    frames=len(angles),
    interval=10,
    blit=True,
)

plt.show()
