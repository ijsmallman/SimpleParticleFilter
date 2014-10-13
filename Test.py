from Terrain import Terrain
from PositionLocator import PositionLocator
import matplotlib.pyplot as plt
from matplotlib import animation
import math

terrain_map = Terrain(4099, 0.8, 0.936846)
height_map = terrain_map.height_map
terrain_map.height_map[1600:1600+700] = [terrain_map.height_map[1600]] * 700
#height_map = [0.1] * 4099
locator = PositionLocator(height_map, 500, 0.0001, 5)

# fig = plt.figure()
# plt.hist(locator.particles, 100)
#
# for i in xrange(0, locator.particle_count):
#     locator.weights[i] = (1/math.sqrt(2*math.pi*locator.obs_noise)) \
#                               * math.exp(-(locator.particles[i]-2000)**2/(2*locator.obs_noise))
#         # normalise weights
# locator.weights = [locator.weights[i]/sum(locator.weights) for i in xrange(0, locator.particle_count)]
#
#
# locator.resample_particles()
# plt.hist(locator.particles, 100)

#locator.find_location()

x = range(0, 4099)
y = height_map

fig = plt.figure()
ax = plt.axes(xlim=(0, 4099), ylim=(0, 1))
points, = ax.plot([], [], '.b')
actPos, = ax.plot([], [], '.r')
#points.set_data(locator.particles, [0.9] * locator.particle_count)

plt.plot(x, y, '.g-')

# initialization function: plot the background of each frame
def init():
    points.set_data([], [])
    actPos.set_data([], [])
    return points, actPos,

# animation function.  This is called sequentially
def animate(i):
    points.set_data(locator.particles, [0.9] * locator.particle_count)
    actPos.set_data(locator.actual_pos, [0.85])
    locator.measure_height()
    locator.find_location()
    locator.move_forward(10)
    return points, actPos,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                              frames=1600, interval=100, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure AttributeError: 'str' object has no attribute 'saving'that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
my_writer = animation.MencoderWriter()
anim.save('basic_animation.mp4', writer = my_writer, fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()

