"""
Matplotlib Animation Example

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")

from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation


# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure(figsize=(14,8))
plt.subplots_adjust(left=0.0, right=1.0,bottom=0.0, top=1.0)
ax = plt.subplot(121, projection='3d')#p3.Axes3D(fig)
ax2 = plt.subplot(122, projection='3d')#p3.Axes3D(fig)
#ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

def linecoords(index, i):
    freq = ([ 0.25 * np.pi * w for w in range(1,9) ]*2)[index]
    if i <= 10:
        return [ 0, np.sin(0.5 * np.pi * i * 0.1), np.cos(0.5 * np.pi * i * 0.1) ]
    elif i > 10 and i <= 110:
        i = i-10
        prec = [ np.sin( freq * i * 0.01), np.cos( freq * i * 0.01), 0 ]
        return prec
    elif i <= 210:
        i = i-110
    elif i > 210:
        i = 100

    prec = [ np.sin(freq * i * 0.01)*np.cos(freq), np.cos(freq * i * 0.01)*np.cos(freq), -np.sin(freq)]
    return prec

# animation function.  This is called sequentially
def animate(i, lines):
    #x = np.linspace(0, 2, 1000)
    #y = np.sin(2 * np.pi * (x - 0.01 * i))
    for index,line in enumerate(lines):
        data = np.empty((3, 2))
        data[:, 0] = (0,0,0)
        data[:, 1] = linecoords(index,i)
        line.set_data(data[0:2,:])
        line.set_3d_properties(data[2, :])
    return lines

lines = [ax.plot([0],[0],[0])[0] for i in range(8)] + [ax2.plot([0],[0],[0])[0] for i in range(8)]

for a in [ax, ax2]:
    a.set_xlim3d([-1.0, 1.0])
    a.set_xlabel('X')

    a.set_ylim3d([-1.0, 1.0])
    a.set_ylabel('Y')

    a.set_zlim3d([-1.0, 1.0])
    a.set_zlabel('Z')
    a.set_title('3D Test')


ax.view_init(10,20)
ax2.view_init(80,20)


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init, fargs = (lines, ),
                               frames=500, interval=20, blit=False)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
