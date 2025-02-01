import numpy as np
from scipy.signal import convolve2d

def make_map(size):
    # Generate a random heightmap using the diamond-square algorithm
    rng = np.random.default_rng()

    max_side = max(size)
    power = int(np.ceil(np.log2(max_side-1)))
    side = int(2**power + 1)
    map = np.zeros((side, side))
    map = np.reshape(range(side*side), (side, side))
    for pow in range(power, 0, -1):
        fullstep = 2**pow
        halfstep = 2**(pow-1)
        # Square step
        corners = map[::fullstep, ::fullstep]
        random_value = rng.random()
        map[halfstep::fullstep, halfstep::fullstep] = convolve2d(corners, np.zeros((2, 2)) + 0.25, mode='valid') + random_value
        # Diamond step
        




print(make_map((20, 20)))
