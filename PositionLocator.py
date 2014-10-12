import random
import numpy as np


class PositionLocator:

    def __init__(self, map, particle_count, obs_noise, move_noise):

        # init map
        self.map = np.asarray(map)
        self.map_width = len(self.map)
        self.particle_count = particle_count
        self.obs_noise = obs_noise
        self.move_noise = move_noise
        self.actual_pos = int(0.1 * self.map_width)
        self.obs_height = 0.0
        self.measure_height()

        # init prior particle distribution to a uniform distribution over map
        # list values are position on map
        # TODO: allow arbitrary prior distribution
        self.particles = np.random.randint(0, int(self.map_width), self.particle_count)
        self.weights = np.ones(self.particle_count) / self.particle_count


    def measure_height(self):
        self.obs_height = self.map[self.actual_pos] + random.gauss(0, self.obs_noise)

    def find_location(self):

        # weight all particles according to observation
        # P(obs|map and obs_noise)
        # assume Gaussian noise with variance = obs_noise
        self.weights = (1.0 / np.sqrt(2*np.pi*self.obs_noise)) \
                            * np.exp(-(self.map[self.particles]-self.obs_height)**2/(2*self.obs_noise))
        # normalise weights
        self.weights = self.weights / sum(self.weights)

        self.resample_particles()
        return

    def resample_particles(self):
        self.particles = np.random.choice(self.particles, self.particle_count, p=self.weights)


    def move_forward(self, n):
        map_width = len(self.map)
        self.particles += n + (np.random.randn(self.particle_count) * self.move_noise).astype(int)
        self.particles %= map_width
        self.actual_pos += n + (np.random.randn(1) * self.move_noise).astype(int)
        self.actual_pos %= map_width

    def move_forward_and_measure_height(self, n):
        self.measure_height()
        self.move_forward(n)




